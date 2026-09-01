import pandas as pd
import matplotlib.pyplot as plt

#le resultados do experimento armazenados no arquivo CSV
dados = pd.read_csv("benchmark.log")

#agrupa medicoes por tamanho da mensagem e calcula RTT medio
medias = dados.groupby("tamanho_bytes")["rtt_ms"].mean()

#exibe no terminal o RTT medio para cada tamanho da mensagem
print("RTT médio por tamanho de mensagem:")

for tamanho, media in medias.items():
    print(f"{tamanho} bytes: {media:.3f} ms")

#cria a figura do gráfico
plt.figure(figsize=(8, 5))

#cria o grafico de barras com o tamanho da mensagem no eixo x e o RTT medio no y
plt.bar(
    [str(tamanho) for tamanho in medias.index],
    medias.values
)

#titulos e eixos do grafico
plt.xlabel("Tamanho da mensagem (bytes)")
plt.ylabel("RTT médio (ms)")
plt.title("RTT médio por tamanho de mensagem")

#ajuste de espacmento
plt.tight_layout()

#salva grafico em imagem
plt.savefig("rtt_medio.png", dpi=300)

print("\nGráfico salvo em rtt_medio.png")