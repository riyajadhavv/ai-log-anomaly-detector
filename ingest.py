import boto3
from datetime import datetime, timedelta
from typing import List, Dict
import re


def fetch_logs(log_group: str, hours: int = 1) -> List[Dict]:
    """
    Fetch log events from AWS CloudWatch for the given log group
    over the last N hours. Returns a list of parsed log entries.
    """
    client = boto3.client("logs")

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    start_ms = int(start_time.timestamp() * 1000)
    end_ms = int(end_time.timestamp() * 1000)

    log_entries = []

    try:
        paginator = client.get_paginator("filter_log_events")
        pages = paginator.paginate(
            logGroupName=log_group,
            startTime=start_ms,
            endTime=end_ms
        )

        for page in pages:
            for event in page.get("events", []):
                parsed = _parse_log_event(event["message"], event["timestamp"])
                if parsed:
                    log_entries.append(parsed)

    except client.exceptions.ResourceNotFoundException:
        return []
    except Exception as e:
        raise RuntimeError(f"Failed to fetch logs from CloudWatch: {str(e)}")

    return log_entries


def _parse_log_event(message: str, timestamp: int) -> Dict:
    """
    Parse a raw log line and extract structured fields.
    Handles common log formats: Apache/Nginx access logs, application logs.
    """
    entry = {
        "timestamp": timestamp,
        "message": message,
        "status_code": None,
        "response_time_ms": None,
        "is_error": False,
        "level": "INFO"
    }

    # Match HTTP status codes (e.g. 200, 404, 500)
    status_match = re.search(r'\b([2-5]\d{2})\b', message)
    if status_match:
        code = int(status_match.group(1))
        entry["status_code"] = code
        entry["is_error"] = code >= 400

    # Match response time in ms (e.g. "235ms" or "235 ms")
    time_match = re.search(r'(\d+)\s*ms', message)
    if time_match:
        entry["response_time_ms"] = int(time_match.group(1))

    # Detect log level
    message_upper = message.upper()
    if "ERROR" in message_upper or "CRITICAL" in message_upper:
        entry["level"] = "ERROR"
        entry["is_error"] = True
    elif "WARN" in message_upper:
        entry["level"] = "WARN"

    return entry
