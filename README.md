# Servidor de Transcodificação de Documentos
**Equipe:** 5

## Descrição do Projeto
Este projeto implementa um serviço centralizado com arquitetura Cliente-Servidor (RPC), capaz de receber um documento Markdown em blocos via streaming gRPC, verificar a integridade da transmissão e transcodificá-lo para HTML.

## Decisão Tecnológica
* **Comunicação RPC**: **gRPC** com **Protocol Buffers** (`.proto`). O protocolo define um contrato tipado entre cliente e servidor usando *client-side streaming*, permitindo enviar arquivos em chunks.
* **Linguagem e Motor de Conversão**: **Python** com `grpcio` e `grpcio-tools`. O motor de conversão usa a biblioteca `markdown` para transformar Markdown em HTML.
* **Concorrência**: O servidor usa `ThreadPoolExecutor` com 10 workers, isolando chamadas simultâneas em threads independentes.

## Controle de Integridade
O protocolo garante que o arquivo é recebido em sua totalidade antes de iniciar a conversão:
1. O cliente informa `total_size` no primeiro chunk enviado.
2. O servidor acumula todos os chunks em memória e ao final compara `len(conteúdo_recebido) == total_size`.
3. Se houver disparidade, retorna `integrity_ok=False` e não realiza a conversão.

## Estrutura de Pastas
```
transcodificador-de-docs/
├── client/
│   └── client.py
├── protos/
│   └── transcoder.proto
├── server/
│   └── server.py
├── stubs/
├── example.md
├── run.sh
├── requirements.txt
└── .gitignore
```

## Como rodar

### 1. Clonar e instalar dependências
```bash
git clone https://github.com/arthurjbc/transcodificador-de-docs.git
cd transcodificador-de-docs
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Gerar os stubs gRPC a partir do .proto
```bash
chmod +x run.sh
./run.sh
```

### 3. Iniciar o servidor
```bash
python3 server/server.py
```

### 4. Enviar um arquivo Markdown e verificar o HTML gerado

Em outro terminal (com o venv ativado):
```bash
python3 client/client.py example.md
```

Para enviar para um servidor remoto:
```bash
python3 client/client.py example.md --host 192.168.1.10:50051
```

### Opções do cliente
```
python3 client/client.py --help
```
