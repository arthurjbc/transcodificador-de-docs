import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'stubs'))

import grpc
import transcoder_pb2
import transcoder_pb2_grpc


def main():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = transcoder_pb2_grpc.TranscoderServiceStub(channel)
        content = b"# teste"
        resp = stub.Convert(transcoder_pb2.ConvertRequest(
            content=content,
            source_format="markdown",
            target_format="html",
            expected_size=len(content),
        ))
        if resp.error_message:
            print('error')
        else:
            print("Conteúdo:")
            print(resp.content.decode('utf-8'))

main()
