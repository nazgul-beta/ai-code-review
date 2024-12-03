from randon.complexity import cc_visit

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
    return prompts
