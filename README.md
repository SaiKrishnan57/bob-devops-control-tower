# Bob DevOps Control Tower

A comprehensive code quality analysis tool powered by IBM Bob and watsonx.ai that provides automated code health assessments, security scanning, and AI-powered recommendations.

## Features

- 🔍 **Static Code Analysis**: Detects code smells, complexity issues, and potential bugs
- 🔐 **Security Scanning**: Identifies hardcoded credentials and unsafe operations
- 🤖 **AI-Powered Summaries**: Leverages IBM watsonx.ai for intelligent executive summaries
- 📊 **Code Health Scoring**: Provides quantitative metrics (0-100 scale)
- 🛠️ **MCP Tool Integration**: Extensible tool framework for custom checks
- 📝 **Detailed Reports**: Generates comprehensive markdown reports

## Prerequisites

- Python 3.8 or higher
- IBM watsonx.ai account (optional, for AI-powered summaries)
- IBM Cloud API key (if using watsonx.ai)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bob-devops-control-tower
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure watsonx.ai (Optional)**
   
   Copy the example environment file:
   ```bash
   cp config.example.env .env
   ```
   
   Edit `.env` and add your IBM watsonx.ai credentials:
   ```env
   WATSONX_API_KEY=your_api_key_here
   WATSONX_PROJECT_ID=your_project_id_here
   WATSONX_URL=https://us-south.ml.cloud.ibm.com
   WATSONX_MODEL_ID=ibm/granite-13b-chat-v2
   ```

## Getting watsonx.ai Credentials

1. **Create an IBM Cloud account**: Visit [IBM Cloud](https://cloud.ibm.com/)
2. **Create a watsonx.ai project**:
   - Navigate to watsonx.ai service
   - Create a new project
   - Copy the Project ID
3. **Generate API Key**:
   - Go to IBM Cloud → Manage → Access (IAM)
   - Create an API key
   - Copy and save it securely

## Usage

### Basic Usage (Without watsonx.ai)

Run the analysis on any Python repository:

```bash
python -m app.main --repo /path/to/your/repository
```

Example:
```bash
python -m app.main --repo ./demo_repo
```

### With watsonx.ai Integration

Once you've configured your `.env` file with watsonx.ai credentials:

```bash
python -m app.main --repo /path/to/your/repository
```

The tool will automatically use watsonx.ai to generate AI-powered executive summaries.

## Output

The tool generates a comprehensive report in `outputs/devops_control_tower_report.md` containing:

1. **Code Health Score**: Overall quality metric (0-100)
2. **Static Code Issues**: Detailed list of detected problems
3. **MCP Tool Findings**: Security and operational concerns
4. **IBM Bob Workflow**: Recommended prompts for code improvement
5. **watsonx.ai Executive Summary**: AI-generated insights and recommendations
6. **Final Recommendations**: Actionable next steps

## Example Output

```
🚀 Bob DevOps Control Tower
--------------------------------
Analyzing repo: ./demo_repo

Files analyzed: 3
Static issues found: 5
MCP-style findings: 2
Code health score: 72/100
Status: Needs Improvement

Report generated: outputs/devops_control_tower_report.md

Next step:
Open the report, then use the IBM Bob prompt inside Bob IDE.
```

## Code Health Scoring

The scoring system evaluates code based on:

- **Critical Issues** (-20 points each): Security vulnerabilities, syntax errors
- **High Severity** (-10 points each): Unsafe operations, major bugs
- **Medium Severity** (-5 points each): Code complexity, maintainability issues
- **Low Severity** (-2 points each): Missing documentation, minor improvements

**Score Ranges:**
- 90-100: Excellent
- 70-89: Good
- 50-69: Needs Improvement
- 0-49: Critical

## Detected Issues

The analyzer detects:

- ✅ Syntax errors
- ✅ Complex functions (>8 statements)
- ✅ Missing documentation
- ✅ Unsafe division operations
- ✅ Hardcoded credentials
- ✅ Potential secrets in code
- ✅ Security vulnerabilities

## Integration with IBM Bob

This tool is designed to work seamlessly with IBM Bob IDE:

1. Run the control tower analysis
2. Review the generated report
3. Use the provided Bob prompt to fix issues
4. Re-run the analysis to verify improvements

## Project Structure

```
bob-devops-control-tower/
├── app/
│   ├── analyzer.py          # Static code analysis
│   ├── file_utils.py        # File reading utilities
│   ├── main.py              # CLI entry point
│   ├── mcp_tools.py         # MCP tool integrations
│   ├── pipeline.py          # Analysis pipeline orchestration
│   ├── reporter.py          # Report generation
│   ├── scorer.py            # Code health scoring
│   ├── watsonx_client.py    # watsonx.ai API client
│   └── watsonx_summary.py   # Summary generation
├── outputs/                 # Generated reports
├── config.example.env       # Example configuration
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Configuration Options

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `WATSONX_API_KEY` | No* | - | IBM watsonx.ai API key |
| `WATSONX_PROJECT_ID` | No* | - | watsonx.ai project ID |
| `WATSONX_URL` | No | `https://us-south.ml.cloud.ibm.com` | watsonx.ai API endpoint |
| `WATSONX_MODEL_ID` | No | `ibm/granite-13b-chat-v2` | Model to use for summaries |
| `WATSONX_MAX_TOKENS` | No | `500` | Maximum tokens in response |
| `WATSONX_TEMPERATURE` | No | `0.7` | Model temperature (0.0-1.0) |

*Required only if you want AI-powered summaries

## Troubleshooting

### watsonx.ai Connection Issues

If you see "Using fallback summary" in your report:

1. Verify your `.env` file exists and contains valid credentials
2. Check your IBM Cloud API key is active
3. Ensure your watsonx.ai project ID is correct
4. Verify network connectivity to IBM Cloud

### Import Errors

If you encounter import errors:

```bash
pip install --upgrade -r requirements.txt
```

### Permission Issues

On Windows, if you encounter permission errors:

```bash
python -m pip install --user -r requirements.txt
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Create an issue in the repository
- Contact the development team
- Check IBM watsonx.ai documentation

## Roadmap

- [ ] Support for additional programming languages
- [ ] Integration with CI/CD pipelines
- [ ] Custom rule configuration
- [ ] Web dashboard for reports
- [ ] Team collaboration features
- [ ] Historical trend analysis

## Acknowledgments

- Built with IBM watsonx.ai
- Powered by IBM Bob IDE
- Inspired by DevOps best practices