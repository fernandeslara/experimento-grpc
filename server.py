import grpc
from concurrent import futures
from datetime import datetime, timezone #precisa para timestamp
import benchmark_pb2
import benchmark_pb2_grpc


class BenchmarkServicer(benchmark_pb2_grpc.BenchmarkServicer):

    def Enviar(self, request, context):
        #tamanho do payload recebido em bytes.
        tamanho = len(request.carga_util)

        #timestamp atual em UTC no formato ISO 8601.
        timestamp = datetime.now(
            timezone.utc
        ).isoformat(timespec="microseconds").replace("+00:00", "Z")

        #exibe no terminal aquelas informações sobre a requisição.
        print(
            f"[servidor] Recebido payload de "
            f"{tamanho} bytes em {timestamp}"
        )

        #retorna ao cliente o tamanho recebido e o timestamp
        return benchmark_pb2.Confirmacao(
            tamanho_bytes=tamanho,
            timestamp=timestamp
        )
        #return benchmark_pb2.Confirmacao(recebido=True)


def servir(host="127.0.0.1", porta=50051):
    servidor = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    benchmark_pb2_grpc.add_BenchmarkServicer_to_server(
        BenchmarkServicer(),
        servidor
    )

    endereco = f"{host}:{porta}"
    servidor.add_insecure_port(endereco)

    servidor.start()

    print(f"Servidor gRPC iniciado em {endereco}")
    print("Aguardando mensagens...")

    servidor.wait_for_termination()


if __name__ == "__main__":
    servir()
