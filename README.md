# ☁️ AWS Cloud Infrastructure Automation

> Automated provisioning and management of AWS cloud resources using Python and Terraform IaC — reducing manual effort, eliminating configuration drift, and accelerating deployment cycles.

---

## 🧩 Overview

This project automates end-to-end AWS infrastructure setup using **Python scripts** and **Terraform Infrastructure-as-Code (IaC)**. It covers provisioning EC2 instances, configuring S3 buckets, managing IAM roles and policies, and ensuring consistent environments across dev, staging, and production.

Built during my internship at **CloudHub, Netherlands** where I managed real AWS environments at scale.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Developer / CI Pipeline             │
└────────────────────────┬────────────────────────────┘
                         │ terraform apply / python script
                         ▼
┌─────────────────────────────────────────────────────┐
│                    AWS Cloud                         │
│                                                      │
│   ┌──────────┐   ┌──────────┐   ┌───────────────┐  │
│   │  EC2     │   │   S3     │   │  IAM Roles    │  │
│   │ Instances│   │ Buckets  │   │  & Policies   │  │
│   └──────────┘   └──────────┘   └───────────────┘  │
│                                                      │
│   ┌──────────────────────────────────────────────┐  │
│   │         VPC · Subnets · Security Groups      │  │
│   └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## ⚙️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python (boto3)** | AWS SDK — scripting and automation |
| **Terraform** | Infrastructure as Code |
| **AWS EC2** | Virtual server provisioning |
| **AWS S3** | Object storage management |
| **AWS IAM** | Access control and policy management |
| **AWS CLI** | Command-line resource management |
| **Linux (Ubuntu)** | Server environment |
| **Git + GitHub** | Version control |

---

## 🚀 Features

- ✅ **One-command provisioning** — spin up a full environment with `terraform apply`
- ✅ **Reusable Terraform modules** — separate modules for EC2, S3, IAM, VPC
- ✅ **Python automation scripts** — boto3-based scripts for routine tasks (start/stop instances, rotate keys, sync S3)
- ✅ **Environment consistency** — same config across dev, staging, prod — zero drift
- ✅ **IAM least-privilege setup** — role-based access, no hardcoded credentials
- ✅ **Remote state management** — Terraform state stored in S3 with DynamoDB locking

---

## 📁 Project Structure

```
aws-cloud-automation/
│
├── terraform/
│   ├── main.tf              # Root module
│   ├── variables.tf         # Input variables
│   ├── outputs.tf           # Output values
│   ├── modules/
│   │   ├── ec2/             # EC2 instance module
│   │   ├── s3/              # S3 bucket module
│   │   ├── iam/             # IAM roles & policies
│   │   └── vpc/             # VPC, subnets, security groups
│
├── scripts/
│   ├── provision.py         # Main provisioning script
│   ├── manage_instances.py  # Start/stop/list EC2 instances
│   ├── s3_sync.py           # S3 bucket sync utility
│   └── iam_audit.py         # IAM policy audit script
│
├── configs/
│   ├── dev.tfvars           # Dev environment variables
│   ├── staging.tfvars       # Staging environment variables
│   └── prod.tfvars          # Production environment variables
│
└── README.md
```

---

## 🔧 Setup & Usage

### Prerequisites
- AWS CLI configured (`aws configure`)
- Terraform >= 1.0
- Python 3.8+ with boto3 (`pip install boto3`)

### Provision Infrastructure
```bash
cd terraform/
terraform init
terraform plan -var-file="configs/dev.tfvars"
terraform apply -var-file="configs/dev.tfvars"
```

### Run Python Automation Scripts
```bash
# List all running EC2 instances
python scripts/manage_instances.py --action list

# Sync local directory to S3
python scripts/s3_sync.py --bucket my-bucket --dir ./data

# Audit IAM policies
python scripts/iam_audit.py --output report.json
```

---

## 📊 Impact

- ⚡ Reduced infrastructure provisioning time by **~60%** vs manual setup
- 🔒 Eliminated hardcoded credentials across all environments
- 🔄 Enabled repeatable, consistent deployments across dev/staging/prod
- 📋 Improved team onboarding — new environments ready in minutes

---

## 🌱 MLOps Extension (In Progress)

Extending this project to support ML workload infrastructure:
- Auto-provisioning GPU EC2 instances for model training
- S3-based model artifact storage with versioning
- IAM roles scoped for SageMaker access
- CloudWatch monitoring for training job metrics

---

## 👩‍💻 Author

**Riya Jadhav** — Cloud & AI Engineer  
📧 riajadhav05@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/riyajadhavv) · [Portfolio](https://riyajadhav.vercel.app)

---

> *Built with real-world experience from CloudHub internship (Netherlands) — managing production AWS environments.*
