import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import argparse
import threading

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'stubs'))

import grpc
import transcoder_pb2
import transcoder_pb2_grpc

CHUNK_SIZE = 1024


def stream_monitor(stub):
    print("Iniciando monitoramento em tempo real...")
    try:
        # Chama o novo endpoint do proto
        for stats in stub.MonitorStats(transcoder_pb2.MonitorRequest()):
            # Limpa a tela (código ANSI) para atualizar o dashboard no terminal
            print("\033[2J\033[H", end="")
            print("--- PAINEL DE MONITORAMENTO ---")
            print(f"Conexões Ativas: {stats.active}")
            print(f"Pico de Concorrência: {stats.peak}")
            print(f"Total de Sucessos: {stats.total}")
            print(f"Total de Falhas: {stats.failed}")
            print(f"Bytes Recebidos: {stats.bytes_in}")
            print(f"Bytes Enviados: {stats.bytes_out}")
    except grpc.RpcError as e:
        print(f"\nStream de monitoramento fechado: {e.details()}")

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

    channel = grpc.insecure_channel(args.host)
    stub = transcoder_pb2_grpc.TranscoderServiceStub(channel)


    if args.monitor:
        threading.Thread(target=stream_monitor, args=(stub,), daemon=True).start()

    if args.file:
        send_file(stub, args.file, args.source, args.target, args.out)
    elif not args.monitor:
        parser.print_help()
    
    if args.monitor:
        try:
            input("Pressione Enter para sair...\n")
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()