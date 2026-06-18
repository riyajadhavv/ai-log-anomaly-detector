import boto3
import json
import os
from datetime import datetime


def send_alert(log_group: str, score: float, summary: str):
    """
    Send an alert when an anomaly is detected.
    Publishes to AWS SNS topic for email/Slack/PagerDuty integration.
    Falls back to CloudWatch custom metric if SNS is not configured.
    """
    alert_payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "log_group": log_group,
        "anomaly_score": round(score, 4),
        "summary": summary,
        "severity": _get_severity(score)
    }

    sns_topic_arn = os.getenv("SNS_TOPIC_ARN")

    if sns_topic_arn:
        _publish_sns(sns_topic_arn, alert_payload)
    else:
        _publish_cloudwatch_metric(alert_payload)

    print(f"[ALERT] {alert_payload['severity']} anomaly detected in {log_group}: {summary}")


def _publish_sns(topic_arn: str, payload: dict):
    """Publish alert to AWS SNS — triggers email, Slack, or PagerDuty."""
    try:
        sns = boto3.client("sns")
        sns.publish(
            TopicArn=topic_arn,
            Subject=f"[ANOMALY ALERT] {payload['severity']} — {payload['log_group']}",
            Message=json.dumps(payload, indent=2)
        )
    except Exception as e:
        print(f"[WARNING] SNS publish failed: {e}")


def _publish_cloudwatch_metric(payload: dict):
    """Put a custom CloudWatch metric so alert is visible in AWS console."""
    try:
        cw = boto3.client("cloudwatch")
        cw.put_metric_data(
            Namespace="AnomalyDetector",
            MetricData=[
                {
                    "MetricName": "AnomalyDetected",
                    "Value": 1,
                    "Unit": "Count",
                    "Dimensions": [
                        {"Name": "LogGroup", "Value": payload["log_group"]},
                        {"Name": "Severity", "Value": payload["severity"]}
                    ]
                }
            ]
        )
    except Exception as e:
        print(f"[WARNING] CloudWatch metric publish failed: {e}")


def _get_severity(score: float) -> str:
    if score < -0.4:
        return "CRITICAL"
    elif score < -0.2:
        return "HIGH"
    elif score < -0.1:
        return "MEDIUM"
    else:
        return "LOW"
