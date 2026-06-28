import logging
from concurrent import futures

import grpc
import transcoder_pb2_grpc

import configs as configs
from concurrency import ConversionManager
from servicer import TranscoderServicer

logger = logging.getLogger(__name__)


def serve():
    manager = ConversionManager(configs.MAX_CONCURRENT_CONVERSIONS)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=configs.MAX_WORKERS))
    transcoder_pb2_grpc.add_TranscoderServiceServicer_to_server(
        TranscoderServicer(manager), server
    )
    server.add_insecure_port(configs.ADDRESS)
    server.start()
    logger.info(
        f"servidor gRPC na porta {configs.PORT} "
        f"(workers={configs.MAX_WORKERS}, "
        f"conversões simultâneas={configs.MAX_CONCURRENT_CONVERSIONS})"
    )
    server.wait_for_termination()
