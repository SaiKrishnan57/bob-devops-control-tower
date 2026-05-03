from app.file_utils import read_python_files
from app.analyzer import analyze_code
from app.scorer import calculate_score
from app.reporter import generate_report
from app.mcp_tools import scan_for_secrets
from app.watsonx_client import get_watsonx_client


def run_pipeline(repo_path: str) -> dict:
    """
    Run the Bob DevOps Control Tower pipeline.

    Steps:
    1. Read Python files from the target repo
    2. Run static code analysis
    3. Calculate code health score
    4. Run MCP-style local tool checks
    5. Generate watsonx.ai executive summary
    6. Create final markdown report
    """

    files = read_python_files(repo_path)

    issues = analyze_code(files)

    score_data = calculate_score(issues)

    mcp_findings = scan_for_secrets(files)

    watson_client = get_watsonx_client()

    if watson_client:
        watsonx_summary = watson_client.generate_summary(
            issues=issues,
            score_data=score_data,
            mcp_findings=mcp_findings
        )
    else:
        watsonx_summary = """
## watsonx.ai Executive Summary

watsonx.ai was not configured successfully, so the pipeline could not generate an AI-powered executive summary.

Please check:
- WATSONX_API_KEY
- WATSONX_PROJECT_ID
- WATSONX_URL
"""

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