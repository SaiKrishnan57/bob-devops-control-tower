import ast


def analyze_code(files: dict) -> list:
    issues = []

    for file_name, content in files.items():
        try:
            tree = ast.parse(content)
        except SyntaxError as error:
            issues.append({
                "file": file_name,
                "type": "Syntax Error",
                "severity": "High",
                "message": str(error)
            })
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if len(node.body) > 8:
                    issues.append({
                        "file": file_name,
                        "type": "Complex Function",
                        "severity": "Medium",
                        "message": f"Function '{node.name}' may be too complex."
                    })

                if not ast.get_docstring(node):
                    issues.append({
                        "file": file_name,
                        "type": "Missing Documentation",
                        "severity": "Low",
                        "message": f"Function '{node.name}' has no docstring."
                    })

            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
                issues.append({
                    "file": file_name,
                    "type": "Unsafe Division",
                    "severity": "High",
                    "message": "Division operation found. Check for zero-division handling."
                })

            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if "admin123" in node.value or "password" in node.value.lower():
                    issues.append({
                        "file": file_name,
                        "type": "Hardcoded Credential",
                        "severity": "Critical",
                        "message": "Potential hardcoded credential found."
                    })

    return issues