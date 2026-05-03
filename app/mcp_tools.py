from pathlib import Path
import subprocess
import difflib


def scan_for_secrets(files: dict) -> list:
    findings = []

    secret_keywords = [
        "password",
        "secret",
        "api_key",
        "token",
        "admin123"
    ]

    for file_name, content in files.items():
        for line_number, line in enumerate(content.splitlines(), start=1):
            lowered = line.lower()
            if any(keyword in lowered for keyword in secret_keywords):
                findings.append({
                    "tool": "secret_scanner",
                    "file": file_name,
                    "line": line_number,
                    "finding": "Possible secret or credential-like value detected."
                })

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