from cyclomatic_complexity import CodeRiskAnalyzer
from ASTAnalyzer import ASTLayer

def prioritize_file(changed_files):
/*************  ✨ Codeium Command ⭐  *************/
    """
    Prioritizes the given changed files based on risk and complexity.

    Args:
        changed_files (list): List of dictionaries containing information about 
                              the changed files, including "path" and "diff".

    Returns:
        list: Sorted list of dictionaries with analysis results for each file, 
              including risk and complexity scores. The files are sorted in 
              descending order based on risk and complexity.
    """
/******  01065750-d7c0-4c9b-abe7-296dee5698ae  *******/
    prioritized_files = []

    for file_info in changed_files:
        file_analysis = CodeRiskAnalyzer(file_info["path"], file_info["diff"]).analyze();
        file_analysis["diff"] = file_info["diff"]
        if file_analysis:
            prioritized_files.append(file_analysis)
    
    #Sort on the basis on higher risk and complexity
    prioritized_files.sort(key=lambda x: (x["high_risk"], x["complexity"]), reverse=True)
    return prioritized_files

def augment_files(changed_files, top_files):
/*************  ✨ Codeium Command ⭐  *************/
    """
    Augment the given changed files with risk, complexity, functions, classes, imports and docstrings information using CodeRiskAnalyzer and ASTLayer.

    Args:
        changed_files (list): List of dictionaries containing information about the changed files (path, diff)
        top_files (int): Number of top files to take based on risk for review

    Returns:
        list: List of dictionaries containing information about the changed files augmented with risk, complexity, functions, classes, imports and docstrings
    """
/******  c6c6823a-87b6-4b5a-9b60-332e98f9dc4c  *******/
    prioritized_files = prioritize_file(changed_files)

    # Take top files based on risk(HOTSPOTS) for review & do analysis using AST
    for file in prioritized_files[:top_files]:
        analysis_result = ASTLayer(file["path"])._analyze()
        file['functions']=analysis_result['functions']
        file['classes']=analysis_result['classes']
        file['imports']=analysis_result['imports']
        file['docstrings']=analysis_result['docstrings']
        # print(f"File: {file['path']}")
        # print(f"High Risk: {file['high_risk']}")
        # print(f"Complexity: {file['complexity']}")
        # print(f"Diff: {file['diff']}")
        # print(f"Functions: {file['functions']}")
        # print(f"Classes: {file['classes']}")
        # print(f"Imports: {file['imports']}")
        # print(f"Docstrings: {file['docstrings']}")
        # print("-" * 50)


    #Files containing information like risk, complexity, functions, classes, imports, docstrings to augment the LLM
    return prioritized_files


# if __name__ == "__main__":
#     changed_files = [
#         {"path": "./test-data/auth_service.py", "diff": "password, secret, token, auth, JWT, login, logout, verify_user, authenticate, ACL, role, permission, MD5, SHA1, RSA, AES, hmac, key, decrypt, en"},
#         {"path": "./test-data/utils.py", "diff": "Code change 2"},
#         {"path": "./test-data/payment_processor.py", "diff": "Code change 3"},  
#         {"path": "./test-data/data_processor.py", "diff": "Code change 4"},
#         {"path": "./test-data/file_handler.py", "diff": "Code change 5"},
#         {"path": "./test-data/data_processor.py", "diff": "Code change 6"},
#         {"path": "./test-data/security_manager.py", "diff": "Code change 7"},
#     ]

#     augmented_files = augment_files(changed_files, top_files=3)
    
    



