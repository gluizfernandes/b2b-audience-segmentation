import numpy as np
import pandas as pd


def generate_b2b_engagement_data(
    n_events: int = 8000,
    n_companies: int = 1000,
    random_state: int = 42,
) -> pd.DataFrame:
    """Generate simulated B2B ad engagement logs."""
    rng = np.random.default_rng(random_state)
    ids = [f"ID_CORP_{i:04d}" for i in range(1, n_companies + 1)]

    return pd.DataFrame({
        "company_id": rng.choice(ids, n_events),
        "impressions": 1,
        "clicks": rng.choice([0, 1], n_events, p=[0.96, 0.04]),
        "cost": rng.uniform(0.8, 12.0, n_events),
        # session_duration in seconds; gamma reflects real dwell-time distribution
        "session_duration": rng.gamma(shape=2, scale=50, size=n_events),
    })
