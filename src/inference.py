import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


CLUSTER_ACTIONS = {
    0: "Maximizar budget + criar Lookalike Audiences com esse perfil",
    1: "Remover de paid media, capturar via retargeting, nutrir por e-mail",
    2: "Negativar palavras-chave ou A/B test 14 dias; excluir se CTR não melhorar",
}


def save_model(
    kmeans: KMeans,
    scaler: StandardScaler,
    model_path: str = "models/modelo_b2b.pkl",
    scaler_path: str = "models/scaler_b2b.pkl",
) -> None:
    joblib.dump(kmeans, model_path)
    joblib.dump(scaler, scaler_path)


def load_model(
    model_path: str = "models/modelo_b2b.pkl",
    scaler_path: str = "models/scaler_b2b.pkl",
) -> tuple[KMeans, StandardScaler]:
    return joblib.load(model_path), joblib.load(scaler_path)


def predict_cluster(
    company_data: dict,
    kmeans: KMeans,
    scaler: StandardScaler,
    features: list[str],
) -> int:
    """Classify a single company into a cluster and return the cluster id."""
    X = pd.DataFrame([company_data])[features]
    X_scaled = scaler.transform(X)
    return int(kmeans.predict(X_scaled)[0])


def classify_and_act(
    company_data: dict,
    kmeans: KMeans,
    scaler: StandardScaler,
    features: list[str],
) -> dict:
    """Return cluster id and the recommended media action."""
    cluster_id = predict_cluster(company_data, kmeans, scaler, features)
    return {
        "cluster": cluster_id,
        "action": CLUSTER_ACTIONS[cluster_id],
    }
