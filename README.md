# Experimento de Desempenho com gRPC

Experimento desenvolvido para a disciplina de Sistemas Distribuídos,
com o objetivo de avaliar o desempenho de chamadas gRPC em Python
utilizando diferentes tamanhos de payload.
Grupo do trabalho: Maria Fernanda, Lara, Estela e Anna.

## Objetivo

Medir RTT de chamadas gRPC para mensagens de:

- 1 byte
- 10.000 bytes
- 100.000 bytes
- 1.000.000 bytes

Para cada tamanho são realizadas 20 chamadas, totalizando 80 requisições.

## Estrutura do projeto

- `benchmark.proto` — define o contrato da comunicação gRPC.
- `benchmark_pb2.py` — código Python gerado a partir do `.proto`.
- `benchmark_pb2_grpc.py` — classes gRPC geradas a partir do `.proto`.
- `server.py` — implementação do servidor gRPC.
- `client.py` — implementação do cliente e execução do benchmark.
- `benchmark.log` — registro dos resultados do experimento.

## Tecnologias

- Python 3
- gRPC
- WSL/Linux

## Execução


### Servidor

ative o ambiente virtual
python3 server.py

### Cliente

(em outro terminal e ative o ambiente virtual também)
python client.py --servidor <ip>:<porta>
O cliente realiza as 80 chamadas e as registra no log.(benchmark.log)

### Análise

(em andamento)