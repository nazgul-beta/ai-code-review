import ast

class ASTLayer:
    def __init__(self, file_path):

        with open(file_path, 'r') as file:
                self.code = file.read()
                self.tree = ast.parse(self.code)

        self.analysis_results = {
            "functions":[],
            "classes":[],
            "imports":[],
            "docstrings":{"module":None, "functions":[], "classes":[]}
        }

    def _analyze(self):
        """
        Perform a single traversal of the AST and populate analysis results.
        Get all functions, classes, imports, complexity, and docstrings.
        """

        self.analysis_results["docstrings"]["module"] = ast.get_docstring(self.tree)

        #*now traverse the ast tree
        for node in ast.walk(self.tree):

            #Let us know about the all FUNCTIONS present in this file. Yay!
            if isinstance(node, ast.FunctionDef):
                func_details = {
                    "node":node.name,
                    #node.args.args accesses the function's arguments
                    "args":[arg.arg for arg in node.args.args],
                    "docstring":ast.get_docstring(node)
                }

                self.analysis_results["functions"].append(func_details)

                if func_details["docstring"]:
                    self.analysis_results["docstrings"]["functions"].append({
                        "name":func_details["node"],
                        "docstring":func_details["docstring"]
                    })

            #Let us know about the all CLASSES present in this file. Yay!
            elif isinstance(node, ast.ClassDef):
                #Add class details
                methods=[
                    subnode.name for subnode in node.body if isinstance(subnode, ast.FunctionDef)
                ]

                class_details = {
                    "name":node.name,
                    "docstring":ast.get_docstring(node),
                    "methods":methods
                }

                self.analysis_results["classes"].append(class_details)

                if class_details["docstring"]:
                    self.analysis_results["docstrings"]["classes"].append({
                        "name": class_details["name"],
                        "docstring":class_details["docstring"]
                    })

            #Let us know about the all IMPORTS present in this file. Yay!
            elif isinstance(node, ast.Import):

                for alias in node.names:
                    self.analysis_results["imports"].append({
                        "type":"import",
                        "module":alias.name
                    })

            elif isinstance(node, ast.ImportFrom):
                self.analysis_results["imports"].append({
                    "type":"from-import",
                    "module":node.module,
                    "names":[alias.name for alias in node.names]
                })

        return self.analysis_results



if __name__ == "__main__":
    file_path = "./test-data/auth_service.py"
    analyzer = ASTLayer(file_path)
    result = analyzer._analyze()
    print(result)