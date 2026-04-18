#!/bin/bash

cd /home/ubuntu/quotes-scraper

source venv/bin/activate

python3 scraper.py >> logs.txt 2>&1