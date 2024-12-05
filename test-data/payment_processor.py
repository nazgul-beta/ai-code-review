# payment_processor.py
# This file has:
# - Risky file I/O operations (e.g., reading sensitive data).
# - API calls with no error handling (e.g., payment gateway interaction).
# - Potential data corruption during transaction logging.

import json
import os
import requests

def read_api_key():
    # Risk: Reads sensitive API key from a file without access control
    with open("api_key.txt", "r") as f:
        return f.read().strip()

def process_payment(amount, user_id):
    # Risk: No error handling for payment API - could result in undetected failures
    api_key = read_api_key()
    response = requests.post(
        "https://paymentgateway.com/api/charge",
        json={"amount": amount, "user_id": user_id},
        headers={"Authorization": f"Bearer {api_key}"}
    )
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Payment processing failed")

def log_transaction(user_id, amount):
    # Risk: Writes transaction logs without validation - risk of data corruption
    with open("transactions.log", "a") as f:
        f.write(f"{user_id}: {amount}\n")
