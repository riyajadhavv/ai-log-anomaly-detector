import pandas as pd
from typing import List, Dict


def extract_features(log_entries: List[Dict]) -> pd.DataFrame:
    """
    Convert raw log entries into numerical features for Isolation Forest.
    Groups logs into 1-minute windows and computes aggregated stats per window.
    """
    df = pd.DataFrame(log_entries)

    # Convert timestamp (ms) to datetime
    df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df.sort_values("datetime")

    # Resample into 1-minute windows
    df.set_index("datetime", inplace=True)
    features = df.resample("1min").agg(
        total_requests=("message", "count"),
        error_count=("is_error", "sum"),
        avg_response_time=("response_time_ms", "mean"),
        max_response_time=("response_time_ms", "max"),
        error_rate=("is_error", "mean"),
        status_5xx=("status_code", lambda x: (x >= 500).sum()),
        status_4xx=("status_code", lambda x: ((x >= 400) & (x < 500)).sum()),
    ).reset_index()

    # Fill NaN response times with 0
    features["avg_response_time"] = features["avg_response_time"].fillna(0)
    features["max_response_time"] = features["max_response_time"].fillna(0)

    # Drop rows where no requests were made
    features = features[features["total_requests"] > 0].reset_index(drop=True)

    return features


def get_feature_matrix(features_df: pd.DataFrame) -> pd.DataFrame:
    """
    Return only the numerical columns used for Isolation Forest training/prediction.
    """
    feature_cols = [
        "total_requests",
        "error_count",
        "avg_response_time",
        "max_response_time",
        "error_rate",
        "status_5xx",
        "status_4xx"
    ]
    return features_df[feature_cols].fillna(0)
