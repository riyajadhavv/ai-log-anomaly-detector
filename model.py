import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from pipeline.features import get_feature_matrix
from typing import Tuple
import joblib
import os

MODEL_PATH = "configs/model.pkl"


class AnomalyDetector:
    """
    Isolation Forest-based anomaly detector for CloudWatch log features.
    Trains on the incoming data (unsupervised) and scores each window.
    Anomaly score < threshold means anomaly detected.
    """

    def __init__(self, contamination: float = 0.05, threshold: float = -0.1):
        self.contamination = contamination
        self.threshold = threshold
        self.model = IsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=42
        )
        self._load_model()

    def predict(self, features_df: pd.DataFrame) -> Tuple[float, bool]:
        """
        Train on all windows, score the latest window.
        Returns (anomaly_score, is_anomaly).
        Anomaly score: closer to -1 = more anomalous, closer to 0 = normal.
        """
        X = get_feature_matrix(features_df)

        if len(X) < 5:
            return 0.0, False

        # Fit on all data (unsupervised — no labels needed)
        self.model.fit(X)

        # Score the most recent window
        latest = X.iloc[[-1]]
        score = self.model.score_samples(latest)[0]
        is_anomaly = score < self.threshold

        self._save_model()

        return float(score), bool(is_anomaly)

    def _save_model(self):
        try:
            joblib.dump(self.model, MODEL_PATH)
        except Exception:
            pass

    def _load_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
            except Exception:
                pass
