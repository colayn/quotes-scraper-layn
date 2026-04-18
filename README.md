## 🚀 Pipeline Execution Flow

This project is designed to run on an **Ubuntu Linux EC2 instance** and follows a simple, reproducible data pipeline.

---

### 🟢 Step 1 — Connect to EC2 Instance

```bash
ssh -i your-key.pem ubuntu@3.106.115.232
```

### 🟢 Step 2 — Clone Repository

```bash
git clone https://github.com/colayn/quotes-scraper-layn.git
cd quotes-scraper-layn
```

### 🟢 Step 3 — Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate   # Linux / Ubuntu / macOS
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
playwright install chromium
```

### 🟢 Step 4 — Configure AWS Credentials

```bash
aws configure
```

### 🟢 Step 5 — Run the Pipeline

```bash
aws configure
```

### 🟢 Step 6 — Verify the Output

```bash
cat quotes_output.json
```

## BONUS — Automate Daily Execution

```bash
crontab -e
```

### Add:
```bash
0 8 * * * /home/ubuntu/quotes-scraper-layn/run_scraper.sh
```

📊 Pipeline Overview

```bash
EC2 (Ubuntu)
    ↓
Python (venv)
    ↓
Playwright Scraper
    ↓
JSON Output
    ↓
AWS S3 Upload
```