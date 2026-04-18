# ☁️ Quotes Scraper Pipeline (Part 2 - AWS Automation)

## 📌 Overview

This project extends the Quotes Scraper into a full cloud-based data pipeline using AWS.

It automates:
- Web scraping (Playwright)
- Data processing (Python)
- Cloud storage (AWS S3)
- Cloud compute (AWS EC2)
- Optional scheduling (cron)

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
(Optional) Cron Job Scheduler
```

---

## ⚙️ Tech Stack

- Python 3
- Playwright (Sync API)
- boto3 (AWS SDK)
- AWS EC2
- AWS S3
- Ubuntu Linux
- Cron (automation)

---

# 🚀 Setup Guide

---

## 🟢 1. Create AWS EC2 Instance

Go to AWS Console → EC2 → Launch Instance

### Configuration:
- Name: `quotes-scraper-ec2`
- OS: Ubuntu 24.04
- Instance type: `t3.micro` (Free Tier)
- Key pair: create/download `.pem` # <your-key>.pem
- Storage: default (8 GB)

  a. Go to EC2 dashboard

  b. Wait until status = running

### Security Group:
| Type | Port | Source |
|------|------|--------|
| SSH | 22 | Your IP |

---

## 🟢 2. Create AWS S3 Bucket

Go to AWS Console → S3 → Create Bucket

- Settings:
- Bucket name: `quotes-scraper-s3`
- Region: same as EC2
- Block public access: ON (default)

## 🟢 3. CREATE IAM ROLE (AWS CONSOLE)

Go to:
👉 AWS Console → IAM → Roles → Create Role

Select:
- Trusted entity: AWS Service
- Use case: EC2
  
Click Next.

### Attach permissions:
Search and select:
```bash
AmazonS3FullAccess
```

### Name the role:
```bash
EC2-S3-Scraper-Role
```
Create role.

✔ This removes the need for aws configure

## 🟢 4. ATTACH ROLE TO YOUR EC2 INSTANCE

Go to:

👉 EC2 → Instances → your instance

Then:

👉 Actions → Security → Modify IAM Role

Select:
- EC2-S3-Scraper-Role

Click save.
  

## 🟢5. Connect to EC2

```bash
chmod 400 <your-key>.pem
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
```
This key is not known by any other names. Are you sure you want to continue connecting (yes/no/[fingerprint])?

### Type:
```bash
yes
```
Then press Enter

### Output should be:
```bash
ubuntu@ip-172-31-xx-xx:~$
```

## 🟢6. Install system dependencies

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

### AWS CLI Install
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip -y
unzip awscliv2.zip
sudo ./aws/install
aws --version
```

## 🟢7. Clone repository

```bash
git clone https://github.com/colayn/quotes-scraper-part2.git
cd quotes-scraper-part2
```

### Create virtual environment & install dependencies

```bash
python3 -m venv venv
source venv/bin/activate   # Linux / macOS
# venv\Scripts\activate    # Windows
```

```bash
pip install -r requirements.txt
playwright install chromium
```

## 🟢8. Run full pipeline

```bash
python scraper.py
```
### Expected Output:

```bash
Found 49 authors
Processing...
Saved quotes_output.json
Uploaded → s3://your-bucket/quotes_output.json
```
## 🟢9. Verify in AWS

```bash
aws s3 cp s3://quotes-scraper-s3/quotes_output.json -
```
## (BONUS) Cron Job - Automation

- Open cron editor on EC2
```bash
crontab -e
```

### Add:
- This runs at 7:00 AM server time (PH)
```bash
23 23 * * * cd /home/ubuntu/quotes-scraper-part2 && /home/ubuntu/quotes-scraper-part2/venv/bin/python scraper.py >> /home/ubuntu/quotes-scraper-part2/cron.log 2>&1
```

### Verify cron was saved

```bash
crontab -l
```

Make sure it shows
```bash
23 23 * * * cd /home/ubuntu/quotes-scraper-part2 && /home/ubuntu/quotes-scraper-part2/venv/bin/python scraper.py >> /home/ubuntu/quotes-scraper-part2/cron.log 2>&1
```

# Repository Structure
```bash
quotes-scraper-part2/
│
├── scraper.py
├── aws
|   ├── s3_upload.py
├── requirements.txt
├── README.md
│
├── venv/ (NOT INCLUDED IN GIT)
└── cron.log (auto-generated)
```
