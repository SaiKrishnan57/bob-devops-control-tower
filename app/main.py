import argparse
from app.pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser(
        description="Bob DevOps Control Tower CLI"
    )

    parser.add_argument(
        "--repo",
        required=True,
        help="Path to the repository you want to analyze"
    )

    args = parser.parse_args()

    print("\nBob DevOps Control Tower")
    print("--------------------------------")
    print(f"Analyzing repo: {args.repo}\n")
    
    result = run_pipeline(args.repo)

    print(f"Files analyzed: {result['files_analyzed']}")
    print(f"Static issues found: {len(result['issues'])}")
    print(f"MCP-style findings: {len(result['mcp_findings'])}")
    print(f"Code health score: {result['score']['score']}/100")
    print(f"Status: {result['score']['status']}")
    print(f"\nReport generated: {result['report_path']}")

    print("\nNext step:")
    print("Open the report, then use the IBM Bob prompt inside Bob IDE.")


if __name__ == "__main__":
    main()