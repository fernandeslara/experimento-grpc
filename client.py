import grpc

import benchmark_pb2
import benchmark_pb2_grpc


def executar():
    with grpc.insecure_channel("10.0.1.11:50051") as canal:
        stub = benchmark_pb2_grpc.BenchmarkStub(canal)

        mensagem = benchmark_pb2.Mensagem(
            carga_util=b"Hello gRPC!"
        )

        resposta = stub.Enviar(mensagem)

        print(f"Confirmação recebida: {resposta.recebido}")


if __name__ == "__main__":
    executar()
