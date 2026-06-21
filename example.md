# Exemplo de Documento Markdown

Este é um arquivo de exemplo para testar o servidor de transcodificação.

## Introdução

O **servidor gRPC** recebe arquivos em blocos via *streaming* e os converte para HTML.

## Funcionalidades

- Recepção de arquivos em chunks de 1 KB
- Validação de integridade por comparação de tamanho
- Conversão Markdown → HTML
- Suporte a múltiplos clientes simultâneos

## Exemplo de código

```python
stub.ConvertStream(chunks)
```

## Tabela de formatos suportados

| Origem   | Destino |
|----------|---------|
| markdown | html    |
