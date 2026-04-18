#!/bin/bash

cd /home/ubuntu/quotes-scraper-part2

source venv/bin/activate

python3 scraper.py >> logs.txt 2>&1
