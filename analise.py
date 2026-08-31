import pandas as pd
import matplotlib.pyplot as plt

dados = pd.read_csv("benchmark.log")

medias = dados.groupby("tamanho_bytes")["rtt_ms"].mean()

print("RTT médio por tamanho de mensagem:")

for tamanho, media in medias.items():
    print(f"{tamanho} bytes: {media:.3f} ms")

plt.figure(figsize=(8, 5))

plt.bar(
    [str(tamanho) for tamanho in medias.index],
    medias.values
)

plt.xlabel("Tamanho da mensagem (bytes)")
plt.ylabel("RTT médio (ms)")
plt.title("RTT médio por tamanho de mensagem")

plt.tight_layout()

plt.savefig("rtt_medio.png", dpi=300)

print("\nGráfico salvo em rtt_medio.png")