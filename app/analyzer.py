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
                # Check for actual hardcoded credentials, not just the word "password"
                # Exclude environment variable names and common non-secret patterns
                value_lower = node.value.lower()
                
                # Skip if it's an environment variable name (all caps with underscores)
                if node.value.isupper() and '_' in node.value:
                    continue
                
                # Skip if it's just a parameter name or role name
                if node.value in ["admin", "manager", "user", "username", "password"]:
                    continue
                    
                # Flag actual suspicious patterns
                suspicious_patterns = [
                    "admin123",
                    "password123",
                    "secret123",
                    "apikey",
                ]
                
                # Check for patterns like "password=" or "secret=" with actual values
                if any(pattern in value_lower for pattern in suspicious_patterns):
                    issues.append({
                        "file": file_name,
                        "type": "Hardcoded Credential",
                        "severity": "Critical",
                        "message": f"Potential hardcoded credential found: {node.value[:20]}..."
                    })
                # Check for assignment-like patterns (e.g., "password=something")
                elif ("=" in node.value and any(kw in value_lower for kw in ["password", "secret", "token", "key"])):
                    issues.append({
                        "file": file_name,
                        "type": "Hardcoded Credential",
                        "severity": "Critical",
                        "message": "Potential hardcoded credential in assignment pattern."
                    })

    return issues