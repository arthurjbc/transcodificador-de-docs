# Servidor de Transcodificação de Documentos
**Disciplina:** Sistemas Distribuídos  
**Equipe:** 05  

## Descrição do Projeto
Este projeto implementa um serviço centralizado com arquitetura Cliente-Servidor (RPC), capaz de receber um documento bruto em Markdown, verificar a integridade de sua transmissão e transcodificá-lo para HTML. 

## Decisão Tecnológica
* **Comunicação RPC**: Adotamos o framework **gRPC** juntamente com o **Protocol Buffers** (`.proto`). O protocolo atende ao requisito de garantir as transações criando um contrato tipado rigoroso entre o cliente e o servidor, sendo ideal para trafegar o binário bruto do arquivo (`bytes`).
* **Linguagem e Motor de Conversão**: A linguagem escolhida foi **Python**, integrada com `grpcio` e `grpcio-tools` por sua simplicidade para compilação de stubs de rede. O motor de conversão textual utiliza a biblioteca nativa `markdown` para mapear de forma prática a lógica entre os formatos, permitindo à equipe manter o foco na topologia distribuída.

## Controle de Integridade
O protocolo garante que o arquivo é recebido em sua totalidade (100%) antes de começar a usar o processamento da CPU:
1. O cliente encapsula a requisição via método `Convert`, preenchendo obrigatoriamente a propriedade `expected_size` com o tamanho local do byte array.
2. O servidor (`server.py`) analisa a requisição e valida de forma restrita se o `len(request.content)` diverge de `request.expected_size`.
3. Em caso de disparidade, o fluxo é imediatamente abortado, devolvendo uma resposta de erro (`integrity_ok=False`), não permitindo que a transformação ocorra em dados com perdas de pacotes.

## Arquitetura e Estrutura de Pastas
```
transcodificador-de-docs/
├── client/                
│   └── client.py                  # Script executável simulando o cliente (Envia arquivo para teste)
├── protos/
│   └── transcoder.proto           # Definição do contrato gRPC (mensagens e campos)
├── server/                
│   └── server.py                  # Lógica do servidor (Roteamento RPC, Integridade e Conversão)    
├── run.sh                         # Script bash automatizando a compilação via protoc
├── requirements.txt               # Dependências do projeto
└── .gitignore
```
## Como rodar
1 - pip install -r requirements.txt
2 - bash run.sh
3 - python server.py
4 - python client.py
