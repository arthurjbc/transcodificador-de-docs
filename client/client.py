import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'stubs'))

import grpc
import transcoder_pb2
import transcoder_pb2_grpc

CHUNK_SIZE = 1024


def chunk_generator(content, source_format, target_format):
    total_size = len(content)
    for offset in range(0, total_size, CHUNK_SIZE):
        chunk_data = content[offset:offset + CHUNK_SIZE]
        yield transcoder_pb2.FileChunk(
            data=chunk_data,
            source_format=source_format if offset == 0 else "",
            target_format=target_format if offset == 0 else "",
            total_size=total_size if offset == 0 else 0,
        )
        print(f"  chunk {offset // CHUNK_SIZE + 1}: {len(chunk_data)} bytes")


def save_output(content, filepath, target_format, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(filepath))[0]
    out_path = os.path.join(out_dir, f"{base}.{"html"}")
    with open(out_path, "wb") as f:
        f.write(content)
    return out_path


def send_file(filepath, source_format, target_format, host, out_dir):
    with open(filepath, 'rb') as f:
        content = f.read()

    print(f"enviando {filepath} ({len(content)} bytes) para {host}")

    with grpc.insecure_channel(host) as channel:
        stub = transcoder_pb2_grpc.TranscoderServiceStub(channel)
        try:
            response = stub.ConvertStream(chunk_generator(content, source_format, target_format))
        except grpc.RpcError as e:
            print(f"erro2: [{e.code()}] {e.details()}")
            sys.exit(1)

    if response.error_message:
        print(f"erro1: {response.error_message}")
        sys.exit(1)

    print(f"\nintegridade: {'ok' if response.integrity_ok else 'falhou'}")
    print(f"saída: {response.output_size} bytes")

    out_path = save_output(response.content, filepath, target_format, out_dir)
    print(f"salvo em: {out_path}")


def main():
    parser = argparse.ArgumentParser(description="cliente gRPC para transcodificação de documentos")
    parser.add_argument("file")
    parser.add_argument("--source", default="markdown")
    parser.add_argument("--target", default="html")
    parser.add_argument("--host", default="localhost:50051")
    parser.add_argument("--out", default="output", help="pasta de destino do arquivo convertido")
    args = parser.parse_args()

    send_file(args.file, args.source, args.target, args.host, args.out)

main()
