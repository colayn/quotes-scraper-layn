# ☁️ Quotes Scraper Pipeline (Part 2 - AWS Automation)

## 📌 Overview

This project extends the Quotes Scraper into a complete cloud-based data pipeline using AWS.

It automates:
- Web scraping (Playwright)
- Data processing (Python)
- Cloud storage (AWS S3)
- Cloud compute (AWS EC2)
- Scheduling (Cron)

---

## 🏗️ Architecture

```bash
EC2 Instance (Ubuntu Server)
            ↓
Playwright Scraper (Python)
            ↓
    JSON Output File
            ↓
      boto3 Upload
            ↓
AWS S3 Bucket (Cloud Storage)
            ↓
(Cron - Daily Automation)
```

---

## ⚙️ Tech Stack

- Python 3
- Playwright
- boto3 (AWS SDK)
- AWS EC2
- AWS S3
- Ubuntu Linux
- Cron

---

# 🚀 Setup Guide

---

## 🟢 1. Create AWS EC2 Instance

👉 Go to AWS Console → EC2 → Launch Instance

### Configuration:
- Name: `quotes-scraper-ec2`
- OS: Ubuntu 24.04
- Instance type: `t3.micro` (Free Tier)
- Key pair: create/download `.pem` # <your-key>.pem
- Storage: default (8 GB)

### Security Group:
| Type | Port | Source |
|------|------|--------|
| SSH | 22 | Your IP |

Wait until instance status = **Running**

---

## 🟢 2. Create S3 Bucket

👉 Go to AWS Console → S3 → Create Bucket

- Settings:
- Bucket name: `quotes-scraper-s3`
- Region: same as EC2
- Keep default settings

## 🟢 3. Create IAM Role

Go to:
👉 AWS Console → IAM → Roles → Create Role

Select:
- Trusted entity: AWS Service
- Use case: EC2
- Service: EC2
- Permissions: `AmazonS3FullAccess`
- Name: `EC2-S3-Scraper-Role`
  
Create role.

✔ This removes the need for aws configure

## 🟢 4. Attach Role to EC2

Go to:
👉 EC2 → Instances → Actions → Security → Modify IAM Role  

Select:
- EC2-S3-Scraper-Role  

## 🟢 5. Connect to EC2

```bash
chmod 400 <your-key>.pem
ssh -i <your-key>.pem ubuntu@<EC2_PUBLIC_IP>
```

This key is not known by any other names. Are you sure you want to continue connecting (yes/no/[fingerprint])?
### Type:
```bash
yes
```
### Output should be:
```bash
ubuntu@ip-172-31-xx-xx:~$
```

## 🟢 6. Install system dependencies

```bash
sudo apt update

sudo apt install -y \
    python3-venv \
    libatk1.0-0t64 \
    libatk-bridge2.0-0t64 \
    libcups2t64 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2t64 \
    libpangocairo-1.0-0 \
    libnss3 \
    libxss1 \
    libgtk-3-0t64 \
    libdrm2 \
    libx11-xcb1 \
    libxcb1
```

## 🟢 7. Clone repository

```bash
git clone https://github.com/colayn/quotes-scraper-part2.git
cd quotes-scraper-part2
```

## 🟢 8. Setup Environment

```bash
python3 -m venv venv
source venv/bin/activate   # Linux / macOS
# venv\Scripts\activate    # Windows
```

```bash
pip install -r requirements.txt
playwright install chromium
```

## 🟢 9. Run full pipeline

```bash
python scraper.py
```
### Expected Output:

```bash
Found 49 authors
Saved quotes_output.json
Uploaded → s3://your-bucket/quotes_output.json
```
## 🟢9. Verify Output in S3

```bash
aws s3 cp s3://quotes-scraper-s3/quotes_output.json -
```

## ⏱️ (BONUS) Schedule Daily Execution

- Edit cron
```bash
crontab -e
```

### Add:

```bash
23 23 * * * cd /home/ubuntu/quotes-scraper-part2 && /home/ubuntu/quotes-scraper-part2/venv/bin/python scraper.py >> /home/ubuntu/quotes-scraper-part2/cron.log 2>&1
```
🕒 Time Explanation
- Server timezone: UTC
- Philippines: UTC +8
- 23:23 UTC = 7:23 AM PH

### Verify cron:

```bash
crontab -l
```

# Repository Structure
```bash
quotes-scraper-part2/
│
├── scraper.py
├── aws/
│   └── s3_upload.py
├── requirements.txt
├── README.md
│
├── venv/ (excluded)
└── cron.log (generated)
```
