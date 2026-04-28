import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def aggregate_by_company(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate event-level logs into company-level engagement metrics."""
    agg = (
        raw_df.groupby("company_id")
        .agg(
            total_impressions=("impressions", "sum"),
            total_clicks=("clicks", "sum"),
            total_cost=("cost", "sum"),
            avg_session_seconds=("session_duration", "mean"),
        )
        .reset_index()
    )

    agg["ctr"] = agg["total_clicks"] / agg["total_impressions"] * 100
    # Companies with zero clicks still incur cost; use total_cost as proxy
    agg["cpc"] = agg.apply(
        lambda r: r["total_cost"] / r["total_clicks"]
        if r["total_clicks"] > 0
        else r["total_cost"],
        axis=1,
    )
    agg["avg_time_site"] = agg["avg_session_seconds"] / 60

    return agg.drop(columns=["avg_session_seconds"])


def remove_outliers(
    df: pd.DataFrame,
    columns: list[str],
    percentile: float = 99,
) -> pd.DataFrame:
    """Remove rows above the given percentile in any of the specified columns.

    Percentile 99 (not 95) preserves more of the high-CTR tail that is
    behaviorally meaningful for Cluster 0 (high-performance accounts).
    """
    mask = pd.Series(True, index=df.index)
    for col in columns:
        ceiling = df[col].quantile(percentile / 100)
        mask &= df[col] <= ceiling
    return df[mask].copy()


def scale_features(
    df: pd.DataFrame,
    features: list[str],
) -> tuple[np.ndarray, StandardScaler]:
    """Standardise features to zero mean and unit variance."""
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[features])
    return X_scaled, scaler
