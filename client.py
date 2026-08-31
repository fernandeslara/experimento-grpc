import argparse  # Lê argumentos do terminal
import csv       # Grava os resultados em CSV
import time      # Mede o tempo das chamadas
from datetime import datetime, timezone  # Gera timestamps em UTC

import grpc  # Biblioteca gRPC

import benchmark_pb2       # Mensagens definidas no .proto
import benchmark_pb2_grpc  # Stub e serviços gRPC

# Tamanhos de payload em bytes
TAMANHOS = [1, 10000, 100000, 1000000]

# Quantidade de chamadas para cada tamanho
NUM_CHAMADAS = 20


def executar(endereco_servidor):

    # Abre o canal de comunicação com o servidor
    with grpc.insecure_channel(endereco_servidor) as canal:

        # Cria o stub usado para chamar o método remoto
        stub = benchmark_pb2_grpc.BenchmarkStub(canal)

        # Cria o arquivo de resultados
        with open("benchmark.log", "w", newline="") as arquivo:

            # Objeto para escrita em CSV
            writer = csv.writer(arquivo)

            # Cabeçalho do arquivo
            writer.writerow([
                "timestamp",
                "tamanho_bytes",
                "indice_chamada",
                "rtt_ms"
            ])

            # Testa cada tamanho de payload
            for tamanho in TAMANHOS:

                # Cria o payload com o tamanho desejado
                payload = b"x" * tamanho

                # Cria a mensagem Protobuf
                mensagem = benchmark_pb2.Mensagem(
                    carga_util=payload
                )

                # Repete a chamada 20 vezes
                for indice in range(1, NUM_CHAMADAS + 1):

                    # Marca o início da medição
                    inicio = time.perf_counter()

                    # Envia a mensagem e recebe a resposta
                    resposta = stub.Enviar(mensagem)

                    # Marca o fim da medição
                    fim = time.perf_counter()

                    # Calcula o RTT em milissegundos
                    rtt_ms = (fim - inicio) * 1000

                    # Salva a medição no arquivo
                    writer.writerow([
                        resposta.timestamp,
                        resposta.tamanho_bytes,
                        indice,
                        rtt_ms
                    ])

                    # Mostra o resultado no terminal
                    print(
                        f"Tamanho: {tamanho} bytes | "
                        f"Chamada: {indice}/20 | "
                        f"RTT: {rtt_ms:.3f} ms"
                    )


# Executa apenas quando o arquivo é iniciado diretamente
if __name__ == "__main__":

    # Cria o leitor de argumentos do terminal
    parser = argparse.ArgumentParser()

    # Define o endereço do servidor
    parser.add_argument(
        "--servidor",
        default="10.0.1.11:50051",
        help="Endereço IP e porta do servidor gRPC"
    )

    # Lê os argumentos informados
    args = parser.parse_args()

    # Inicia o experimento
    executar(args.servidor)