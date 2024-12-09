# data_processor.py

# Risky patterns:
# Regex usage (re.findall)
# API calls (requests.get)
# Potential for mishandling API responses

import re
import requests

def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

def fetch_data_from_api(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    return None

def process_data(data):
    if not data:
        return []
    return [item.strip().lower() for item in data]
