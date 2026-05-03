from pathlib import Path
import subprocess
import difflib


def scan_for_secrets(files: dict) -> list:
    """
    Scan for potential hardcoded secrets with improved false positive reduction.
    
    Excludes:
    - Environment variable names (UPPER_CASE_WITH_UNDERSCORES)
    - Comments and docstrings explaining security
    - Test fixture mock values
    - Function parameter names
    """
    findings = []

    # Patterns that indicate actual hardcoded secrets
    suspicious_patterns = [
        "admin123",
        "password123",
        "secret123",
        "Bearer ",
        "Basic ",
    ]
    
    # Patterns to check with context (need assignment or quotes)
    contextual_keywords = ["api_key", "apikey", "token", "secret", "password"]

    for file_name, content in files.items():
        lines = content.splitlines()
        
        for line_number, line in enumerate(lines, start=1):
            stripped = line.strip()
            lowered = line.lower()
            
            # Skip comments that are just explaining security practices
            if stripped.startswith('#') and any(word in lowered for word in ['should', 'must', 'nosec', 'credentials', 'environment']):
                continue
            
            # Skip docstrings
            if '"""' in line or "'''" in line:
                continue
                
            # Skip environment variable names (all caps with underscores)
            if any(word.isupper() and '_' in word for word in stripped.split()):
                # Check if it's just a variable name, not an assignment
                if '=' not in stripped or 'os.getenv' in stripped or 'environ' in stripped:
                    continue
            
            # Skip test file mock/patch decorators
            if '@patch' in line or 'patch.dict' in line:
                continue
            
            # Check for obvious suspicious patterns
            if any(pattern in line for pattern in suspicious_patterns):
                findings.append({
                    "tool": "secret_scanner",
                    "file": file_name,
                    "line": line_number,
                    "finding": "Hardcoded credential pattern detected."
                })
                continue
            
            # Check for contextual patterns (assignment with suspicious keywords)
            for keyword in contextual_keywords:
                if keyword in lowered:
                    # Only flag if it looks like an actual assignment with a value
                    if '=' in line and '"' in line and 'getenv' not in lowered and 'environ' not in lowered:
                        # Check if there's an actual value being assigned (not just empty string)
                        parts = line.split('=')
                        if len(parts) > 1:
                            value_part = parts[1].strip()
                            # Skip if it's getting from environment or is a placeholder
                            if value_part and not value_part.startswith('os.') and '""' not in value_part and "''" not in value_part:
                                findings.append({
                                    "tool": "secret_scanner",
                                    "file": file_name,
                                    "line": line_number,
                                    "finding": f"Possible hardcoded {keyword} in assignment."
                                })
                                break

    return findings


def generate_diff(before_path: str, after_path: str) -> str:
    before = Path(before_path).read_text(encoding="utf-8").splitlines()
    after = Path(after_path).read_text(encoding="utf-8").splitlines()

    diff = difflib.unified_diff(
        before,
        after,
        fromfile="before.py",
        tofile="after.py",
        lineterm=""
    )

    return "\n".join(diff)


def run_tests(repo_path: str) -> dict:
    repo = Path(repo_path)

    try:
        result = subprocess.run(
            ["python", "-m", "pytest"],
            cwd=repo,
            capture_output=True,
            text=True,
            timeout=20
        )

        return {
            "tool": "test_runner",
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except FileNotFoundError:
        return {
            "tool": "test_runner",
            "success": False,
            "stdout": "",
            "stderr": "pytest is not installed."
        }

    except subprocess.TimeoutExpired:
        return {
            "tool": "test_runner",
            "success": False,
            "stdout": "",
            "stderr": "Test execution timed out."
        }