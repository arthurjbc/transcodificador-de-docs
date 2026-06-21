import sys
import os
import logging

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'stubs'))

from concurrent import futures
import grpc
import markdown
import transcoder_pb2
import transcoder_pb2_grpc

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)


class TranscoderServicer(transcoder_pb2_grpc.TranscoderServiceServicer):
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
                    logger.info(f"[{client}] {source_format} -> {target_format}, {total_size} bytes esperados")

                chunks.append(chunk.data)
                received_bytes += len(chunk.data)
                logger.info(f"[{client}] chunk recebido: {len(chunk.data)} bytes ({received_bytes}/{total_size})")

            full_content = b"".join(chunks)

            if total_size == 0 or len(full_content) != total_size:
                logger.warning(f"[{client}] integridade falhou: recebido {len(full_content)}, esperado {total_size}")
                return transcoder_pb2.ConvertResponse(
                    content=b"",
                    output_size=0,
                    integrity_ok=False,
                    error_message=f"integridade falhou: recebido {len(full_content)} bytes, esperado {total_size}",
                )

            if source_format != 'markdown' or target_format != 'html':
                msg = f"conversão de '{source_format}' para '{target_format}' não suportada"
                logger.error(f"[{client}] {msg}")
                context.set_code(grpc.StatusCode.UNIMPLEMENTED)
                context.set_details(msg)
                return transcoder_pb2.ConvertResponse(
                    content=b"",
                    output_size=0,
                    integrity_ok=False,
                    error_message=msg,
                )

            source_text = full_content.decode('utf-8')
            output = markdown.markdown(source_text)
            output_bytes = output.encode('utf-8')

            logger.info(f"[{client}] conversão ok: {len(full_content)} -> {len(output_bytes)} bytes")
            logger.info(f"[{client}] HTML gerado:\n{output}")

            return transcoder_pb2.ConvertResponse(
                content=output_bytes,
                output_size=len(output_bytes),
                integrity_ok=True,
                error_message="",
            )

        except Exception as exc:
            logger.exception(f"[{client}] erro inesperado")
            return transcoder_pb2.ConvertResponse(
                content=b"",
                output_size=0,
                integrity_ok=False,
                error_message=str(exc),
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transcoder_pb2_grpc.add_TranscoderServiceServicer_to_server(TranscoderServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    logger.info("servidor gRPC na porta 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
