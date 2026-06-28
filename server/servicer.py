import logging
import time
import grpc
import transcoder_pb2
import transcoder_pb2_grpc

import converter

logger = logging.getLogger(__name__)


class TranscoderServicer(transcoder_pb2_grpc.TranscoderServiceServicer):
    def __init__(self, manager):
        self._manager = manager

    def MonitorStats(self, request, context):
        client = context.peer()
        logger.info(f"[{client}] iniciou stream de monitoramento")
        
        try:
            while context.is_active():
                stats = self._manager.snapshot()
                yield transcoder_pb2.StatsResponse(**stats)
                time.sleep(1)
        except Exception as exc:
            logger.error(f"[{client}] erro no stream de monitoramento: {exc}")
        finally:
            logger.info(f"[{client}] encerrou stream de monitoramento")

    def ConvertStream(self, request_iterator, context):
        client = context.peer()
        chunks = []
        source_format = None
        target_format = None
        total_size = 0
        received_bytes = 0

        try:
            for chunk in request_iterator:
                if source_format is None:
                    source_format = chunk.source_format
                    target_format = chunk.target_format
                    total_size = chunk.total_size
                    logger.info(
                        f"[{client}] {source_format} -> {target_format}, "
                        f"{total_size} bytes esperados"
                    )

                chunks.append(chunk.data)
                received_bytes += len(chunk.data)
                logger.info(
                    f"[{client}] chunk recebido: {len(chunk.data)} bytes "
                    f"({received_bytes}/{total_size})"
                )

            full_content = b"".join(chunks)

            if total_size == 0 or len(full_content) != total_size:
                logger.warning(
                    f"[{client}] integridade falhou: recebido "
                    f"{len(full_content)}, esperado {total_size}"
                )
                self._manager.record_failure()
                return self._error(
                    f"integridade falhou: recebido {len(full_content)} bytes, "
                    f"esperado {total_size}"
                )

            with self._manager.slot():
                try:
                    output_bytes = converter.convert(
                        source_format, target_format, full_content
                    )
                except NotImplementedError as exc:
                    logger.error(f"[{client}] {exc}")
                    self._manager.record_failure()
                    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
                    context.set_details(str(exc))
                    return self._error(str(exc))

            self._manager.record_success(len(full_content), len(output_bytes))
            stats = self._manager.snapshot()
            logger.info(
                f"[{client}] conversão ok: {len(full_content)} -> "
                f"{len(output_bytes)} bytes | ativas={stats['active']} "
                f"pico={stats['peak']} total={stats['total']}"
            )

            return transcoder_pb2.ConvertResponse(
                content=output_bytes,
                output_size=len(output_bytes),
                integrity_ok=True,
                error_message="",
            )

        except Exception as exc:
            logger.exception(f"[{client}] erro inesperado")
            self._manager.record_failure()
            return self._error(str(exc))

    @staticmethod
    def _error(message):
        return transcoder_pb2.ConvertResponse(
            content=b"",
            output_size=0,
            integrity_ok=False,
            error_message=message,
        )
