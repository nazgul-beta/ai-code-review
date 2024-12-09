# security_manager.py
# This file has:
# - Insecure usage of `eval` and dynamic imports.
# - Poor session management with hardcoded secrets.
# - High cyclomatic complexity due to branching in `validate_session`.

import jwt

def execute_dynamic_code(code):
    # Risk: Direct use of eval allows execution of arbitrary code
    return eval(code)

def validate_session(token):
    # Risk: Hardcoded secret for JWT validation
    secret = "static_secret_key"
    try:
        decoded = jwt.decode(token, secret, algorithms=["HS256"])
        if "user_id" in decoded:
            return True
        return False
    except Exception as e:
        return False

def dynamic_import(module_name):
    # Risk: Dynamic imports can load unexpected or malicious modules
    module = __import__(module_name)
    return module
