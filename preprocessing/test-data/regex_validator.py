# regex_validator.py
# This file has:
# - Risky regex patterns with catastrophic backtracking potential.
# - Complex regex validation logic increasing cyclomatic complexity.
# - Security risks due to unbounded input handling.

import re

def validate_email(email):
    # Risk: Regex is vulnerable to catastrophic backtracking for malformed input
    pattern = r'^([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$'
    if re.match(pattern, email):
        return True
    return False

def validate_phone(phone):
    # Risk: Overly complex regex with excessive grouping
    pattern = r'^\+?(\d{1,3})[-.●]?(\d{1,4})[-.●]?(\d{1,4})[-.●]?(\d{1,9})$'
    return re.match(pattern, phone) is not None

def validate_inputs(inputs):
    # High cyclomatic complexity due to multiple validations and branching
    results = {}
    for key, value in inputs.items():
        if key == "email":
            results[key] = validate_email(value)
        elif key == "phone":
            results[key] = validate_phone(value)
        else:
            results[key] = "Unknown field"
    return results
