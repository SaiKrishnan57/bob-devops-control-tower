from pathlib import Path
from datetime import datetime


def generate_report(repo_path: str, issues: list, score_data: dict, mcp_findings: list, watsonx_summary: str) -> str:
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    report_path = output_dir / "devops_control_tower_report.md"

    lines = [
        "# Bob DevOps Control Tower Report",
        "",
        f"Generated at: {datetime.now()}",
        f"Repository analyzed: `{repo_path}`",
        "",
        "## 1. Code Health Score",
        "",
        f"**Score:** {score_data['score']}/100",
        f"**Status:** {score_data['status']}",
        "",
        "## 2. Static Code Issues",
        ""
    ]

    if not issues:
        lines.append("No static code issues found.")
    else:
        for index, issue in enumerate(issues, start=1):
            lines.extend([
                f"### {index}. {issue['type']}",
                f"- **File:** `{issue['file']}`",
                f"- **Severity:** {issue['severity']}",
                f"- **Details:** {issue['message']}",
                ""
            ])

    lines.extend([
        "## 3. MCP-Style Tool Findings",
        ""
    ])

    if not mcp_findings:
        lines.append("No MCP-style tool findings detected.")
    else:
        for index, finding in enumerate(mcp_findings, start=1):
            lines.extend([
                f"### {index}. {finding['tool']}",
                f"- **File:** `{finding['file']}`",
                f"- **Line:** {finding['line']}",
                f"- **Finding:** {finding['finding']}",
                ""
            ])

    lines.extend([
        "## 4. IBM Bob Engineering Workflow",
        "",
        "Recommended Bob prompt:",
        "",
        "```text",
        "You are acting as a senior software engineer inside IBM Bob IDE.",
        "",
        "Analyze this repository using the DevOps Control Tower report.",
        "Fix the highest-risk issues first.",
        "Keep the refactor simple and maintainable.",
        "Generate tests for the changed functions.",
        "Explain every change in a before-and-after format.",
        "```",
        "",
        "## 5. watsonx.ai Style Executive Summary",
        "",
        watsonx_summary,
        "",
        "## 6. Final Recommendation",
        "",
        "Re-run this CLI after Bob applies improvements to compare the new code health score against the original score.",
        ""
    ])

    report_path.write_text("\n".join(lines), encoding="utf-8")

    return str(report_path)