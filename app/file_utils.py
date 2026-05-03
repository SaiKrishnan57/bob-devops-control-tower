from pathlib import Path


def read_python_files(repo_path: str) -> dict:
    repo = Path(repo_path)

    if not repo.exists():
        raise FileNotFoundError(f"Repo path does not exist: {repo_path}")

    files = {}

    for file_path in repo.rglob("*.py"):
        if "__pycache__" in str(file_path):
            continue

        relative_path = file_path.relative_to(repo)
        files[str(relative_path)] = file_path.read_text(encoding="utf-8")

    return files