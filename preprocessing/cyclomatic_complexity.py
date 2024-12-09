
#This preprocessor tells the LLM the most probable parts of the code that have errors. Cool!
from radon.complexity import cc_visit


class CodeRiskAnalyzer:
    def __init__(self, file_path, diff):
/*************  ✨ Codeium Command ⭐  *************/
        """
        Initialize the CodeRiskAnalyzer with a file path and a diff string.
        The diff string is expected to be a unified diff format string.
        The high_risk_keywords list contains keywords that are considered to be
        high risk in terms of security, performance, and reliability.
        """
        
/******  d519d8d2-5d66-4486-942e-ab2fb4f91628  *******/
        self.file_path = file_path
        self.diff = diff
        self.high_risk_keywords=[
        "password", "secret", "token", "auth", "JWT", "login", "logout", "verify_user", "authenticate", 
        "ACL", "role", "permission", "MD5", "SHA1", "RSA", "AES", "hmac", "key", "decrypt", "encrypt", 
        "cipher", "hashlib", "eval", "exec", "compile", "os.system", "subprocess.run", "subprocess.Popen", 
        "__import__", "open(", "read(", "write(", "os.remove", "os.unlink", "os.rename", "os.makedirs", 
        "shutil.move", "shutil.rmtree", "re.match", "re.search", "re.compile", "regex", "input", 
        "requests.get", "requests.post", "urllib.request", "fetch", "http", "socket", "api_key", 
        "access_token", "hardcoded", "plaintext", "base64", "static", "hardcoded_password", 
        "default_password", "DEBUG", "print", "log", "threading", "multiprocessing", "asyncio", 
        "concurrent", "locks", "deadlock", "sql", "query", "cursor", "execute", "db", "SELECT", 
        "INSERT", "DELETE", "UPDATE", "cross-site scripting", "csrf", "ssrf", "file upload", 
        "path traversal", "../", "os.environ"
        ]

    def calculate_cyclomatic_complexity(self, file_content):
        functions = cc_visit(file_content) #Analyze functions in the file
        complexity_scores = {func.name: func.complexity for func in functions}
        return complexity_scores
    
    def is_high_risk_change(self):
        return any(keyword in self.diff for keyword in self.high_risk_keywords)


    def analyze(self):
        try:
            with open(self.file_path, 'r') as file:
                file_content = file.read()
                complexity = self.calculate_cyclomatic_complexity(file_content)
                risk_score = sum(complexity.values())
                high_risk = self.is_high_risk_change()

                return {
                    "path":self.file_path,
                    "complexity":risk_score,
                    "high_risk":high_risk
                }
        
        except Exception as e:
            print(f"Error analyzing file {self.file_path}: {e}")
            return None