
#This is a pre-processing step in which the code is scanned for high risk changes
#and the cyclomatic complexity of the code is calculated
#The output of this step is a list of dictionaries containing the file path, complexity score and high risk flag
#The list is then sorted based on the high risk flag and complexity score
# THIS OUTPUT IS THE INPUT FOR THE LLM

from radon.complexity import cc_visit

def calculate_cyclomatic_complexity(file_content):
    #Calculates the complexity of all the functions in the code
    functions = cc_visit(file_content) #Analyze all the functions in the file
    complexity_scores = {func.name: func.complexity for func in functions}
    return complexity_scores


def is_high_risk_change(file_path, diff):
    #Scans the diffs for risky keywords
    
    high_risk_keywords = ["password","auth","open(", "eval(", "re.compile(", "os.system("] #Add more high risk keywords
    return any(keyword in diff for keyword in high_risk_keywords)

def analyze_file(file_path, diff):

    try:
        with open(file_path, 'r') as file:
            content = file.read()
            complexity = calculate_cyclomatic_complexity(content)
            risk_score = sum(complexity.values())
            high_risk = is_high_risk_change(file_path, diff)

            return{
                "path":file_path,
                "complexity":risk_score,
                "high_risk":high_risk
            }
    
    except Exception as e:
        print(f"Error analyzing file {file_path}: {str(e)}")
        return None

def prioritize_file(changed_files):
    #Sort files based on high-risk flags and complexity scores.

    prioritized_files = []

    for file_info in changed_files:
        file_analysis = analyze_file(file_info["path"], file_info["diff"])
        file_analysis["diff"] = file_info["diff"]
        if file_analysis:
            prioritized_files.append(file_analysis)
    
    prioritized_files.sort(key=lambda x: (x["high_risk"], x["complexity"]), reverse=True)
    return prioritized_files


def generate_llm_prompt(prioritized_files):
    #Generate the prompt for the LLM based on the prioritized files.
    prompts = []
    for file in prioritized_files:
        risk_tag="HIGH-RISK" if file["high_risk"] else "NORMAL"
        prompt = f"""
        File: {file["path"]}
        Risk Level: {risk_tag}
        Cyclomatic complexity: {file["complexity"]}
        Analyze the following changes for potential bugs or security issues:
        {file["diff"]}
        """
        prompts.append(prompt)
        # print(prompt)
    return prompts


if __name__ == "__main__":
    changed_files = [
        {"path": "./test-data/auth_service.py", "diff": "password, secret, token, auth, JWT, login, logout, verify_user, authenticate, ACL, role, permission, MD5, SHA1, RSA, AES, hmac, key, decrypt, en"},
        {"path": "./test-data/utils.py", "diff": "Code change 2"},
        {"path": "./test-data/payment_processor.py", "diff": "Code change 3"},  
        {"path": "./test-data/data_processor.py", "diff": "Code change 4"},
        {"path": "./test-data/file_handler.py", "diff": "Code change 5"},
        {"path": "./test-data/data_processor.py", "diff": "Code change 6"},
        {"path": "./test-data/security_manager.py", "diff": "Code change 7"},

    ]
    prioritized_files = prioritize_file(changed_files)
    prompts = generate_llm_prompt(prioritized_files)

    for prompt in prompts:
        print(prompt)

#Output (Output is the prompts that will be fed to the LLM)
# File: ./test-data/auth_service.py
#         Risk Level: HIGH-RISK
#         Cyclomatic complexity: 7
#         Analyze the following changes for potential bugs or security issues:
#         password, secret, token, auth, JWT, login, logout, verify_user, authenticate, ACL, role, permission, MD5, SHA1, RSA, AES, hmac, key, decrypt, en


#         File: ./test-data/data_processor.py
#         Risk Level: NORMAL
#         Cyclomatic complexity: 6
#         Analyze the following changes for potential bugs or security issues:
#         Code change 4


#         File: ./test-data/data_processor.py
#         Risk Level: NORMAL
#         Cyclomatic complexity: 6
#         Analyze the following changes for potential bugs or security issues:
#         Code change 6


#         File: ./test-data/security_manager.py
#         Risk Level: NORMAL
#         Cyclomatic complexity: 5
#         Analyze the following changes for potential bugs or security issues:
#         Code change 7


#         File: ./test-data/utils.py
#         Risk Level: NORMAL
#         Cyclomatic complexity: 4
#         Analyze the following changes for potential bugs or security issues:
#         Code change 2


#         File: ./test-data/payment_processor.py
#         Risk Level: NORMAL
#         Cyclomatic complexity: 4
#         Analyze the following changes for potential bugs or security issues:
#         Code change 3


#         File: ./test-data/file_handler.py
#         Risk Level: NORMAL
#         Cyclomatic complexity: 3
#         Analyze the following changes for potential bugs or security issues:
#         Code change 5
