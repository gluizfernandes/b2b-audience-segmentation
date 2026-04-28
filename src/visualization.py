import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


CLUSTER_NAMES = {
    0: "Alta Performance",
    1: "Alto Custo Estratégico",
    2: "Volume Sem Retorno",
}

CLUSTER_COLORS = {0: "#2563EB", 1: "#F59E0B", 2: "#EF4444"}


def plot_correlation_matrix(df: pd.DataFrame, features: list[str]) -> None:
    matrix = df[features].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Matriz de Correlação: Métricas de Engajamento B2B")
    plt.tight_layout()
    plt.show()


def plot_elbow(wcss: list[float]) -> None:
    plt.figure(figsize=(8, 4))
    plt.plot(range(1, len(wcss) + 1), wcss, "bo-")
    plt.axvline(x=3, color="red", linestyle="--", alpha=0.5, label="k=3 selecionado")
    plt.title("Método do Cotovelo")
    plt.xlabel("Número de Clusters (k)")
    plt.ylabel("Inércia (SQI)")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_clusters_scatter(df: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 6))
    for cluster_id, group in df.groupby("cluster"):
        plt.scatter(
            group["ctr"],
            group["avg_time_site"],
            c=CLUSTER_COLORS[cluster_id],
            label=f"Cluster {cluster_id} — {CLUSTER_NAMES[cluster_id]}",
            alpha=0.6,
            s=40,
        )
    plt.xlabel("CTR (%)")
    plt.ylabel("Tempo Médio no Site (min)")
    plt.title("Dispersão dos Clusters: CTR vs. Tempo Médio no Site")
    plt.legend()
    plt.tight_layout()
    plt.show()
