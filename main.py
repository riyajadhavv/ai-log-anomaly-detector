from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pipeline.ingest import fetch_logs
from pipeline.features import extract_features
from pipeline.model import AnomalyDetector
from pipeline.alerts import send_alert
import yaml

app = FastAPI(
    title="AI Log Anomaly Detector",
    description="ML pipeline to detect anomalies in AWS CloudWatch logs using Isolation Forest",
    version="1.0.0"
)

with open("configs/config.yaml", "r") as f:
    config = yaml.safe_load(f)

detector = AnomalyDetector()


class AnalyzeRequest(BaseModel):
    log_group: str
    hours: int = 1


class AnalyzeResponse(BaseModel):
    anomaly_detected: bool
    score: float
    summary: str
    log_group: str
    hours_analyzed: int


@app.get("/")
def health_check():
    return {"status": "running", "service": "AI Log Anomaly Detector"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_logs(request: AnalyzeRequest):
    """
    Ingest CloudWatch logs, extract features, run Isolation Forest,
    return anomaly flag + score + summary.
    """
    try:
        raw_logs = fetch_logs(request.log_group, request.hours)
        if not raw_logs:
            raise HTTPException(status_code=404, detail="No logs found for the given log group and time range")

        features_df = extract_features(raw_logs)

        score, is_anomaly = detector.predict(features_df)

        summary = _build_summary(is_anomaly, features_df, score)

        if is_anomaly:
            send_alert(
                log_group=request.log_group,
                score=score,
                summary=summary
            )

        return AnalyzeResponse(
            anomaly_detected=is_anomaly,
            score=round(score, 2),
            summary=summary,
            log_group=request.log_group,
            hours_analyzed=request.hours
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


def _build_summary(is_anomaly: bool, features_df, score: float) -> str:
    if not is_anomaly:
        return "Log behavior within normal range. No anomalies detected."

    error_rate = features_df["error_rate"].iloc[-1]
    avg_response = features_df["avg_response_time"].iloc[-1]

    if error_rate > 0.3:
        return f"Spike in error rate detected — {round(error_rate * 100)}% of requests failing (anomaly score: {round(score, 2)})"
    elif avg_response > 2000:
        return f"High response time detected — average {round(avg_response)}ms (anomaly score: {round(score, 2)})"
    else:
        return f"Statistical anomaly detected in log patterns (anomaly score: {round(score, 2)})"
