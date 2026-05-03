"""
watsonx.ai Summary Generator
Integrates with IBM watsonx.ai to generate AI-powered executive summaries
"""

from app.watsonx_client import get_watsonx_client


def generate_watsonx_style_summary(issues: list, score_data: dict, mcp_findings: list) -> str:
    """
    Generate an executive summary using watsonx.ai
    Falls back to basic summary if watsonx is not configured
    
    Args:
        issues: List of code issues found during analysis
        score_data: Dictionary containing score and status
        mcp_findings: List of MCP tool findings
        
    Returns:
        Formatted executive summary as markdown string
    """
    # Try to get watsonx client
    client = get_watsonx_client()
    
    if client:
        # Use watsonx.ai for AI-powered summary
        return client.generate_summary(issues, score_data, mcp_findings)
    else:
        # Fall back to basic summary
        return _generate_basic_summary(issues, score_data, mcp_findings)


def _generate_basic_summary(issues: list, score_data: dict, mcp_findings: list) -> str:
    """Generate a basic summary when watsonx.ai is not available"""
    severity_count = {}

    for issue in issues:
        severity = issue["severity"]
        severity_count[severity] = severity_count.get(severity, 0) + 1

    return f"""
## watsonx.ai Executive Summary

⚠️ *Note: Using basic summary. Configure watsonx.ai credentials for AI-powered analysis.*

The repository was assessed using a Bob-powered engineering workflow supported by MCP-style local tools.

The current code health score is **{score_data['score']}/100**, with the status: **{score_data['status']}**.

### Key Findings:
- **Critical Issues:** {severity_count.get('Critical', 0)}
- **High Severity:** {severity_count.get('High', 0)}
- **Medium Severity:** {severity_count.get('Medium', 0)}
- **Low Severity:** {severity_count.get('Low', 0)}
- **MCP Findings:** {len(mcp_findings)}

### Risk Assessment:
Critical/High issues may affect security, reliability, or runtime stability. Missing documentation reduces maintainability. MCP-style tool checks detected **{len(mcp_findings)}** additional operational findings.

### Recommended Actions:
1. Address critical and high-severity issues first
2. Use IBM Bob to refactor the highest-risk functions
3. Re-run the control tower pipeline to validate improvements
4. Add comprehensive documentation for undocumented functions

---
*To enable AI-powered summaries, configure your watsonx.ai credentials in .env file*
"""