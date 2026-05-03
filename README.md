# Bob DevOps Control Tower

> A comprehensive code quality analysis tool powered by IBM Bob and watsonx.ai that provides automated code health assessments, security scanning, and AI-powered recommendations.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Understanding Results](#-understanding-results)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Roadmap](#-roadmap)

---

## ✨ Features

### Core Capabilities
- 🔍 **Static Code Analysis** - Detects code smells, complexity issues, and potential bugs
- 🔐 **Security Scanning** - Identifies hardcoded credentials and unsafe operations
- 🤖 **AI-Powered Summaries** - Leverages IBM watsonx.ai for intelligent executive summaries
- 📊 **Code Health Scoring** - Provides quantitative metrics (0-100 scale)
- 🛠️ **MCP Tool Integration** - Extensible tool framework for custom checks
- 📝 **Detailed Reports** - Generates comprehensive markdown reports

### User Interfaces
- 🌐 **Modern Web UI** - Beautiful, intuitive web interface with drag-and-drop
- 💻 **Command Line Interface** - Powerful CLI for automation and CI/CD integration

---

## 🚀 Quick Start

### Web UI (Recommended for First-Time Users)

**Windows:**
```bash
start_web_ui.bat
```

**Linux/Mac:**
```bash
./start_web_ui.sh
```

Then open your browser to `http://localhost:5000`

### Command Line

```bash
python -m app.main --repo ./demo_repo
```

See [QUICK_START.md](QUICK_START.md) for a complete walkthrough.

---

## 📦 Installation

### Prerequisites

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **IBM watsonx.ai account** (optional) - For AI-powered summaries
- **IBM Cloud API key** (optional) - If using watsonx.ai

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bob-devops-control-tower
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure watsonx.ai** (Optional - Skip for basic analysis)
   
   Copy the example configuration:
   ```bash
   # Windows
   copy config.example.env .env
   
   # Linux/Mac
   cp config.example.env .env
   ```
   
   Edit `.env` with your credentials:
   ```env
   WATSONX_API_KEY=your_api_key_here
   WATSONX_PROJECT_ID=your_project_id_here
   WATSONX_URL=https://us-south.ml.cloud.ibm.com
   WATSONX_MODEL_ID=ibm/granite-13b-chat-v2
   ```

### Getting watsonx.ai Credentials

Need AI-powered summaries? Follow these steps:

1. **Create IBM Cloud Account** - Visit [IBM Cloud](https://cloud.ibm.com/)
2. **Set up watsonx.ai Project**
   - Navigate to watsonx.ai service
   - Create a new project
   - Copy the Project ID from project settings
3. **Generate API Key**
   - Go to IBM Cloud → Manage → Access (IAM)
   - Click "API keys" → "Create"
   - Copy and save securely (you won't see it again!)

📖 See [WATSONX_SETUP_GUIDE.md](WATSONX_SETUP_GUIDE.md) for detailed instructions with screenshots.

---

## 💡 Usage

### Web UI (Recommended)

**Launch the interface:**
```bash
python web_app.py
```

**Access at:** `http://localhost:5000`

**Key Features:**
- 🎨 Beautiful, modern interface
- 📤 Drag-and-drop file upload
- 📊 Interactive dashboard with real-time results
- 📥 One-click report download
- 🔄 Dual analysis modes (local path or file upload)

📖 See [WEB_UI_GUIDE.md](WEB_UI_GUIDE.md) for detailed web UI documentation.

### Command Line Interface

**Basic analysis:**
```bash
python -m app.main --repo /path/to/your/repository
```

**Example with demo repository:**
```bash
python -m app.main --repo ./demo_repo
```

**Expected output:**
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
```

### Integration with IBM Bob IDE

Seamless workflow for code improvement:

1. **Run Analysis** - Execute control tower on your codebase
2. **Review Report** - Check `outputs/devops_control_tower_report.md`
3. **Apply Fixes** - Use the provided Bob prompt in Bob IDE
4. **Verify** - Re-run analysis to confirm improvements

---

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `WATSONX_API_KEY` | No* | - | IBM watsonx.ai API key |
| `WATSONX_PROJECT_ID` | No* | - | watsonx.ai project ID |
| `WATSONX_URL` | No | `https://us-south.ml.cloud.ibm.com` | watsonx.ai API endpoint |
| `WATSONX_MODEL_ID` | No | `ibm/granite-13b-chat-v2` | Model for AI summaries |
| `WATSONX_MAX_TOKENS` | No | `500` | Maximum tokens in response |
| `WATSONX_TEMPERATURE` | No | `0.7` | Model creativity (0.0-1.0) |

*Required only for AI-powered summaries. Tool works without watsonx.ai configuration.

---

## 📊 Understanding Results

### Report Contents

Generated reports (`outputs/devops_control_tower_report.md`) include:

1. **Code Health Score** - Overall quality metric (0-100)
2. **Static Code Issues** - Detailed list of detected problems
3. **MCP Tool Findings** - Security and operational concerns
4. **IBM Bob Workflow** - Recommended prompts for code improvement
5. **watsonx.ai Executive Summary** - AI-generated insights (if configured)
6. **Final Recommendations** - Actionable next steps

### Code Health Scoring System

**Deduction Rules:**
- **Critical Issues** (-20 points): Security vulnerabilities, syntax errors
- **High Severity** (-10 points): Unsafe operations, major bugs
- **Medium Severity** (-5 points): Code complexity, maintainability issues
- **Low Severity** (-2 points): Missing documentation, minor improvements

**Score Interpretation:**
- 🟢 **90-100: Excellent** - Production-ready code
- 🟡 **70-89: Good** - Minor improvements recommended
- 🟠 **50-69: Needs Improvement** - Significant issues to address
- 🔴 **0-49: Critical** - Major refactoring required

### Detected Issues

The analyzer identifies:

- ✅ Syntax errors and parsing issues
- ✅ Complex functions (>8 statements)
- ✅ Missing or inadequate documentation
- ✅ Unsafe division operations (potential ZeroDivisionError)
- ✅ Hardcoded credentials and API keys
- ✅ Potential secrets in code
- ✅ Security vulnerabilities and unsafe patterns

---


## 📁 Project Structure

```
bob-devops-control-tower/
├── app/                      # Core application modules
│   ├── analyzer.py          # Static code analysis engine
│   ├── file_utils.py        # File reading utilities
│   ├── main.py              # CLI entry point
│   ├── mcp_tools.py         # MCP tool integrations
│   ├── pipeline.py          # Analysis pipeline orchestration
│   ├── reporter.py          # Report generation
│   ├── scorer.py            # Code health scoring logic
│   └── watsonx_client.py    # watsonx.ai API client
├── templates/               # Web UI templates
│   └── index.html           # Main web interface
├── demo_repo/               # Example repository for testing
│   ├── app.py               # Sample application
│   ├── test_app.py          # Sample tests
│   └── REFACTORING_NOTES.md # Refactoring documentation
├── outputs/                 # Generated analysis reports
├── uploads/                 # Temporary upload directory (web UI)
├── web_app.py              # Flask web application
├── config.example.env       # Example environment configuration
├── requirements.txt         # Python dependencies
├── start_web_ui.bat        # Windows launcher script
├── start_web_ui.sh         # Linux/Mac launcher script
├── QUICK_START.md          # Quick start guide
├── WEB_UI_GUIDE.md         # Detailed web UI documentation
├── WATSONX_SETUP_GUIDE.md  # watsonx.ai setup instructions
└── README.md               # This file
```

---

## 🔧 Troubleshooting

### Common Issues

#### watsonx.ai Connection Problems

**Symptom:** Report shows "Using fallback summary"

**Solutions:**
1. ✅ Verify `.env` file exists in project root
2. ✅ Check API key is valid and active in IBM Cloud
3. ✅ Confirm project ID matches your watsonx.ai project
4. ✅ Test network connectivity to IBM Cloud
5. ✅ Review [WATSONX_SETUP_GUIDE.md](WATSONX_SETUP_GUIDE.md)

#### Import/Dependency Errors

**Symptom:** `ModuleNotFoundError` or import failures

**Solution:**
```bash
# Upgrade all dependencies
pip install --upgrade -r requirements.txt

# Or reinstall from scratch
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

#### Permission Issues (Windows)

**Symptom:** Access denied during installation

**Solution:**
```bash
# Install to user directory
python -m pip install --user -r requirements.txt
```

#### Web UI Not Starting

**Symptom:** Port already in use or connection refused

**Solutions:**
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # Linux/Mac

# Use different port
python web_app.py --port 8080
```

#### File Upload Issues

**Symptom:** Upload fails or files not processed

**Solutions:**
1. ✅ Ensure `uploads/` directory exists and is writable
2. ✅ Check file size limits (default: 16MB)
3. ✅ Verify file is a valid Python repository structure

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup

1. **Fork and clone** the repository
2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Contribution Guidelines

- ✅ Follow PEP 8 style guidelines
- ✅ Add tests for new features
- ✅ Update documentation as needed
- ✅ Keep commits atomic and well-described
- ✅ Submit pull requests with clear descriptions

### Areas for Contribution

- 🐛 Bug fixes and issue resolution
- ✨ New analysis rules and detectors
- 📚 Documentation improvements
- 🌐 UI/UX enhancements
- 🧪 Test coverage expansion
- 🔌 Integration with other tools

---

## 🗺️ Roadmap

### Completed ✅
- [x] Core static analysis engine
- [x] Web dashboard interface
- [x] watsonx.ai integration
- [x] Security scanning capabilities
- [x] Code health scoring system

### In Progress 🚧
- [ ] Support for additional programming languages (JavaScript, Java, Go)
- [ ] CI/CD pipeline integration (GitHub Actions, GitLab CI)
- [ ] Custom rule configuration via YAML

### Planned 📋
- [ ] Team collaboration features
- [ ] Historical trend analysis and metrics tracking
- [ ] Real-time code analysis (watch mode)
- [ ] GitHub/GitLab direct integration
- [ ] Docker containerization
- [ ] VS Code extension
- [ ] Slack/Teams notifications
- [ ] Multi-repository analysis

---

## 📄 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## 💬 Support & Community

### Getting Help

- 📖 **Documentation**: Check our guides in the repository
- 🐛 **Bug Reports**: [Create an issue](../../issues/new)
- 💡 **Feature Requests**: [Open a discussion](../../discussions)
- 📧 **Contact**: Reach out to the development team

### Resources

- [IBM watsonx.ai Documentation](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [IBM Bob IDE](https://www.ibm.com/products/watsonx-code-assistant)
- [Python Best Practices](https://docs.python-guide.org/)

---

## 🙏 Acknowledgments

**Built With:**
- [IBM watsonx.ai](https://www.ibm.com/watsonx) - AI-powered insights
- [IBM Bob IDE](https://www.ibm.com/products/watsonx-code-assistant) - Intelligent code assistance
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Python AST](https://docs.python.org/3/library/ast.html) - Code parsing

**Inspired By:**
- DevOps best practices and automation
- Modern code quality tools (SonarQube, CodeClimate)
- AI-assisted development workflows

---

<div align="center">

**Made with ❤️ by the Bob DevOps Control Tower Team**

[⬆ Back to Top](#bob-devops-control-tower)

</div>