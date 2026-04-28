import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def run_elbow_method(
    X_scaled: np.ndarray,
    k_range: range = range(1, 11),
) -> list[float]:
    """Return inertia values for each k to identify the elbow point."""
    return [
        KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
        .fit(X_scaled)
        .inertia_
        for k in k_range
    ]


def fit_kmeans(
    X_scaled: np.ndarray,
    n_clusters: int = 3,
    random_state: int = 42,
) -> KMeans:
    """Fit K-Means and return the trained model."""
    kmeans = KMeans(
        n_clusters=n_clusters,
        init="k-means++",
        n_init=10,
        random_state=random_state,
    )
    kmeans.fit(X_scaled)
    return kmeans


def calculate_silhouette(X_scaled: np.ndarray, labels: np.ndarray) -> float:
    """Return the Silhouette Score for the clustering solution."""
    return silhouette_score(X_scaled, labels)
