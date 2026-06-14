import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'stubs'))

from concurrent import futures
import grpc
import markdown
import transcoder_pb2
import transcoder_pb2_grpc


class TranscoderServicer(transcoder_pb2_grpc.TranscoderServiceServicer):
    def Convert(self, request, context):
        try:
            integrity_ok = True
            if (request.expected_size == 0 or len(request.content) == request.expected_size):
                integrity_ok = False
            source = request.content.decode('utf-8')

            if (request.source_format == 'markdown' and request.target_format == 'html'):
                output = markdown.markdown(source)
            else:
                context.set_code(grpc.StatusCode.UNIMPLEMENTED)
                context.set_details(
                    f"Conversion from {request.source_format} to {request.target_format} not supported"
                )
                return transcoder_pb2.ConvertResponse(
                    content=b"",
                    output_size=0,
                    integrity_ok=False,
                    error_message=f"Conversion from {request.source_format} to {request.target_format} not supported",
                )

            output_bytes = output.encode('utf-8')
            return transcoder_pb2.ConvertResponse(
                content=output_bytes,
                output_size=len(output_bytes),
                integrity_ok=integrity_ok,
                error_message="",
            )
        except Exception as e:
            return transcoder_pb2.ConvertResponse(
                content=b"",
                output_size=0,
                integrity_ok=False,
                error_message=str(e),
            )


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
transcoder_pb2_grpc.add_TranscoderServiceServicer_to_server(
    TranscoderServicer(), server
)
server.add_insecure_port("[::]:50051")
server.start()
print("Servidor GRPC rodando na port 50051")
server.wait_for_termination()

