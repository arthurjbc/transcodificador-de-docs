import os
import sys
import grpc
from web.config import GRPC_SERVER_ADDRESS, CHUNK_SIZE

_STUBS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "stubs")
sys.path.insert(0, _STUBS)

import transcoder_pb2
import transcoder_pb2_grpc

def chunk_generator(content, source_format="markdown", target_format="html"):
    """Gera pedaços do arquivo mantendo o contrato esperado pelo .proto"""
    total_size = len(content)
    for offset in range(0, total_size, CHUNK_SIZE):
        chunk_data = content[offset:offset + CHUNK_SIZE]
        yield transcoder_pb2.FileChunk(
            data=chunk_data,
            source_format=source_format if offset == 0 else "",
            target_format=target_format if offset == 0 else "",
            total_size=total_size if offset == 0 else 0,
        )

def call_convert_stream(file_content):
    """Executa a chamada RPC ConvertStream de forma síncrona"""
    with grpc.insecure_channel(GRPC_SERVER_ADDRESS) as channel:
        stub = transcoder_pb2_grpc.TranscoderServiceStub(channel)
        response = stub.ConvertStream(chunk_generator(file_content))
        return response

def call_monitor_stats():
    """Consome o gerador contínuo de estatísticas (MonitorStats) do gRPC"""
    with grpc.insecure_channel(GRPC_SERVER_ADDRESS) as channel:
        stub = transcoder_pb2_grpc.TranscoderServiceStub(channel)
        for stats in stub.MonitorStats(transcoder_pb2.MonitorRequest()):
            yield stats