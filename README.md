# Servidor de Transcodificação de Documentos
**Equipe:** 05  
**Fase:** Entrega 3 — Interface e Monitoramento

## 📋 Descrição do Projeto
Este projeto implementa um serviço distribuído com arquitetura Cliente-Servidor (RPC), capaz de receber documentos Markdown em blocos via streaming, validar a integridade da transmissão e transcodificá-los para HTML. Na presente fase, o sistema evoluiu para abolir a interação do usuário via console/terminal, introduzindo uma **Interface Web em React** integrada a um intermediário **BFF (Backend For Frontend)** em Flask e um painel de **Monitoramento Concorrente em Tempo Real**.

## 🛠️ Decisão Tecnológica e Arquitetura

* **Comunicação RPC Core**: O ecossistema principal utiliza **gRPC** sobre **HTTP/2** com **Protocol Buffers** (`.proto`). O protocolo atende ao requisito de garantir as transações criando um contrato tipado rigoroso entre o cliente e o servidor, ideal para trafegar dados binários brutos (`bytes`) através de fluxos de streaming.
* **Camada Intermediária (BFF)**: Como os navegadores web possuem restrições nativas para abrir canais gRPC puros, foi desenvolvida uma camada intermediária **BFF em Flask** (`web/`). O BFF atua como um proxy reverso: recebe arquivos do cliente via requisições HTTP multipart comuns, traduz o payload para chamadas de chunks gRPC e repassa as respostas.
* **Interface Gráfica (Frontend)**: Construído em **React**, o frontend fornece uma experiência rica com seletores de arquivo nativos, feedbacks de processamento visuais e um dashboard dinâmico com métricas assíncronas do servidor. O esquema visual adota as cores institucionais do **Centro de Informática (CIn-UFPE)** (Bordô `#900020` e Branco).
* **Gerenciamento Dinâmico de Concorrência e Travas**: 
  * O servidor gerencia chamadas gRPC concorrentes por meio de um `ThreadPoolExecutor` parametrizado.
  * O motor de conversão textual (`markdown`) é protegido por um **Semáforo Limitador** (`BoundedSemaphore`) baseado no total de núcleos da CPU (`os.cpu_count()`), balanceando dinamicamente o uso de processador.
  * As métricas globais e contadores do servidor são totalmente protegidos contra condições de corrida por meio de um **Lock (Mutex)** exclusivo antes da geração de cada snapshot de estado.

## 🔒 Controle de Integridade e Devolução Automatizada
1. O cliente escolhe um arquivo local `.md` que tem seu tamanho medido pelo React.
2. Ao realizar o envio, o servidor gRPC acumula os blocos em memória e valida se `len(conteudo_completo) == total_size`.
3. Se a validação falhar, o servidor aciona a rotina de erro e retorna `integrity_ok=False`, exibindo um alerta vermelho crítico na interface visual do usuário.
4. Caso a validação seja bem-sucedida, o motor processa a conversão, devolve o HTML em bytes para a rede e **o frontend força o salvamento automatizado (download invisível)** do arquivo no disco local do cliente.

## 📂 Estrutura de Pastas Atualizada
```text
transcodificador-de-docs/
├── client/
│   └── client.py          # Cliente antigo de terminal
├── frontend/              # INTERFACE GRÁFICA (NOVO CLIENTE WEB)
│   ├── src/
│   │   ├── components/    # Componentes modulares (FileSelector, ProgressBar, etc.)
│   │   ├── App.jsx        # Hub de estados e conexão SSE/HTTP
│   │   └── main.jsx
│   └── package.json
├── protos/
│   └── transcoder.proto   # Contrato de serviços e mensagens RPC
├── server/                # BACKEND CORE (gRPC SERVER)
│   ├── main.py            
│   ├── server.py
│   ├── servicer.py        # RPC ConvertStream e MonitorStats
│   ├── concurrency.py     # Travas, Mutexes e BoundedSemaphore
│   ├── converter.py       # Conversor Markdown -> HTML
│   └── config.py          # Limites de threads e portas
├── web/                   # BACKEND FOR FRONTEND (BFF FLASK)
│   ├── app.py             # Inicializador da API Web
│   ├── config.py          # Constantes de rede HTTP
│   ├── grpc_client.py     # Consumidor isolado dos stubs gRPC
│   └── routes.py          # Endpoints HTTP (/transcode e /stats)
├── stubs/                 # Código Python gerado automaticamente pelo protoc
└── requirements.txt       # Dependências Python globais do projeto
```
# Como Executar o Projeto

## Passo Inicial: Instalação e Compilação dos Stubs

git clone [https://github.com/arthurjbc/transcodificador-de-docs.git](https://github.com/arthurjbc/transcodificador-de-docs.git)
cd transcodificador-de-docs
python3 -m venv venv
# No Windows: venv\Scripts\activate
source venv/bin/activate
pip install -r requirements.txt

## Compile o arquivo .proto para gerar os arquivos necessários na pasta stubs/:

# Comando compatível com Windows e Linux (com venv ativo):
    python -m grpc_tools.protoc -I./protos --python_out=./stubs --grpc_python_out=./stubs ./protos/transcoder.proto

# Terminal 1: Iniciar o Servidor gRPC Core
    Este é o backend que gerencia o processamento paralelo pesado e as travas de concorrência:

    source venv/bin/activate
    python server/main.py

# Terminal 2: Iniciar o Intermediário BFF (API Flask)
    source venv/bin/activate
    python -m web.app

# Terminal 3: Iniciar a Interface Gráfica (React)
    cd frontend
    npm install
    npm run dev

# Cenários de Teste e Validação das Regras de Domínio

    Dashboard em Tempo Real (SSE): Ao abrir o React, observe os contadores de métricas superiores. Eles se conectam via stream assíncrono ao servidor gRPC e atualizam instantaneamente conforme conexões paralelas acontecem, sem recarregar a tela.

    Fluxo de Conversão e Salvamento Dinâmico: Faça o upload de um arquivo .md válido. A barra de progresso rastreará a transição e, assim que concluído, o arquivo .html equivalente será baixado direto no seu diretório de downloads local automaticamente.

    Tratamento Visual de Erros: Derrube o processo do Terminal 1 (Ctrl + C) e tente fazer um upload pela página. A interface exibirá uma tarja vermelha amigável indicando "Servidor gRPC indisponível", tratando erros de forma clara na interface conforme exigido.