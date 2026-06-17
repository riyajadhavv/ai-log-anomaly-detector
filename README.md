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
