from app.file_utils import read_python_files
from app.analyzer import analyze_code
from app.scorer import calculate_score
from app.reporter import generate_report
from app.mcp_tools import scan_for_secrets
from app.watsonx_summary import generate_watsonx_style_summary


def run_pipeline(repo_path: str) -> dict:
    files = read_python_files(repo_path)

    issues = analyze_code(files)
    score_data = calculate_score(issues)

    mcp_findings = scan_for_secrets(files)

    watsonx_summary = generate_watsonx_style_summary(
        issues=issues,
        score_data=score_data,
        mcp_findings=mcp_findings
    )

    report_path = generate_report(
        repo_path=repo_path,
        issues=issues,
        score_data=score_data,
        mcp_findings=mcp_findings,
        watsonx_summary=watsonx_summary
    )

    return {
        "files_analyzed": len(files),
        "issues": issues,
        "score": score_data,
        "mcp_findings": mcp_findings,
        "watsonx_summary": watsonx_summary,
        "report_path": report_path
    }