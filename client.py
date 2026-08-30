import argparse
import csv
import time
from datetime import datetime, timezone

import grpc

import benchmark_pb2
import benchmark_pb2_grpc


TAMANHOS = [1, 10000, 100000, 1000000]
NUM_CHAMADAS = 20


def executar(endereco_servidor):

    with grpc.insecure_channel(endereco_servidor) as canal:

        stub = benchmark_pb2_grpc.BenchmarkStub(canal)

        with open("benchmark.log", "w", newline="") as arquivo:

            writer = csv.writer(arquivo)

            writer.writerow([
                "timestamp",
                "tamanho_bytes",
                "indice_chamada",
                "rtt_ms"
            ])

            for tamanho in TAMANHOS:

                payload = b"x" * tamanho

                mensagem = benchmark_pb2.Mensagem(
                    carga_util=payload
                )

                for indice in range(1, NUM_CHAMADAS + 1):

                    inicio = time.perf_counter()

                    resposta = stub.Enviar(mensagem)

                    fim = time.perf_counter()

                    rtt_ms = (fim - inicio) * 1000

                    timestamp = datetime.now(
                        timezone.utc
                    ).isoformat()

                    writer.writerow([
                        timestamp,
                        tamanho,
                        indice,
                        rtt_ms
                    ])

                    print(
                        f"Tamanho: {tamanho} bytes | "
                        f"Chamada: {indice}/20 | "
                        f"RTT: {rtt_ms:.3f} ms"
                    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--servidor",
        default="10.0.1.11:50051",
        help="Endereço IP e porta do servidor gRPC"
    )

    args = parser.parse_args()

    executar(args.servidor)
