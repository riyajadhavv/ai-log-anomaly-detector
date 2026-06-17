# 🔍 AI Log Anomaly Detector

ML pipeline to detect anomalies in AWS CloudWatch server logs using Isolation Forest — deployed as a FastAPI service on EC2.

## 🧩 Overview

DevOps teams waste hours manually tailing logs to find incidents. This project automates that process — ingesting AWS CloudWatch logs, extracting features, classifying anomalies using Isolation Forest, and triggering automated alerts proactively.

Built to bridge cloud operations with ML capabilities — no labeled data needed.





## ⚙️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python (boto3) | CloudWatch log ingestion |
| Pandas | Feature extraction & data processing |
| Scikit-learn | Isolation Forest anomaly detection |
| FastAPI | REST API serving the ML model |
| AWS EC2 | Deployment environment |
| AWS CloudWatch | Log source |

## 🚀 Features

✅ Automated log ingestion from AWS CloudWatch using boto3  
✅ Feature engineering — extracts error rate, response time, request count from raw logs  
✅ Unsupervised ML — no labeled data needed, Isolation Forest learns normal behavior  
✅ REST API endpoint — `POST /analyze` returns anomaly flag and confidence score  
✅ Automated alerts — triggered immediately on anomaly detection  
✅ Deployed on EC2 — always running, no manual intervention  


## 🔧 Setup & Usage

**Prerequisites**
- AWS CLI configured (`aws configure`)
- Python 3.8+ with dependencies (`pip install -r requirements.txt`)
- EC2 instance with CloudWatch access via IAM role

**Run the API locally**
```bash
uvicorn api.main:app --reload
```

**Analyze logs**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"log_group": "/aws/ec2/app-logs", "hours": 1}'
```

**Sample Response**
```json
{
  "anomaly_detected": true,
  "score": -0.43,
  "summary": "Spike in error rate detected — 340% above baseline"
}
```

## 📊 How Isolation Forest Works

Isolation Forest is an unsupervised anomaly detection algorithm. It works by randomly splitting data:
- **Normal points** require many splits to isolate — they blend in with the data
- **Anomalous points** get isolated in very few splits — they're statistically "different"

No labeled training data needed — the model learns what normal log behavior looks like and flags deviations automatically.

## 📈 Impact

⚡ Proactive detection — catches anomalies before they become incidents  
🔍 Eliminates manual log tailing for DevOps teams  
🚀 Always-on service deployed on EC2 — zero manual intervention  
📉 Reduces mean time to detect (MTTD) infrastructure issues  

## 👩‍💻 Author

**Riya Jadhav** — Cloud & AI Engineer  
📧 riajadhav05@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/riyajadhavv) · [Portfolio](https://riyaportfolio-henna.vercel.app)
