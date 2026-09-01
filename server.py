import grpc
from concurrent import futures
from datetime import datetime, timezone #precisa para timestamp
import benchmark_pb2 #mensagens definidas no proto
import benchmark_pb2_grpc #classes e funcoes do servico grpc

#serviço benchmark definico pelo benchmark.proto
class BenchmarkServicer(benchmark_pb2_grpc.BenchmarkServicer):

#metodo remoto enviar
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

#cria e inicia o servidor grpc
def servir(host="127.0.0.1", porta=50051):
    servidor = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    #registra o servico no servidor grpc
    benchmark_pb2_grpc.add_BenchmarkServicer_to_server(
        BenchmarkServicer(),
        servidor
    )

    #montagem de endereço no formato
    endereco = f"{host}:{porta}"
    #porta definida pro servidor aceitar conexoes
    servidor.add_insecure_port(endereco)

    servidor.start()

    print(f"Servidor gRPC iniciado em {endereco}")
    print("Aguardando mensagens...")

    #mantem o servidor aberto e aguardando requisicoes
    servidor.wait_for_termination()


if __name__ == "__main__":
    servir()
