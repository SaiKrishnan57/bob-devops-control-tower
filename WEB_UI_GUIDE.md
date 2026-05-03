# Bob DevOps Control Tower - Web UI Guide

## Overview

The Bob DevOps Control Tower now includes a beautiful, modern web interface that provides an intuitive way to analyze your code repositories without using the command line.

## Features

✨ **Modern Design**
- Clean, aesthetic interface with gradient backgrounds
- Responsive layout that works on all devices
- Smooth animations and transitions
- IBM Carbon Design System inspired

🔍 **Dual Analysis Modes**
- **Local Path**: Analyze repositories on your local machine
- **File Upload**: Upload Python files directly for analysis

📊 **Interactive Dashboard**
- Real-time code health score display
- Visual metrics cards showing:
  - Files analyzed
  - Issues found
  - Security findings
- Color-coded issue severity indicators
- Detailed issue breakdown with file locations

🎯 **Key Capabilities**
- Instant analysis results
- Download full markdown reports
- Error handling with user-friendly messages
- Loading states for better UX

## Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment Variables** (Optional)
   ```bash
   # Copy the example config
   cp config.example.env .env
   
   # Edit .env with your watsonx.ai credentials (optional)
   # The web UI works without watsonx.ai, but you'll get AI-powered insights with it
   ```

## Running the Web UI

### Start the Server

```bash
python web_app.py
```

The server will start at `http://localhost:5000`

### Access the Interface

Open your web browser and navigate to:
```
http://localhost:5000
```

## Using the Web UI

### Method 1: Analyze Local Repository

1. Click on the **"Local Path"** tab (default)
2. Enter the path to your repository (e.g., `./demo_repo` or `C:/path/to/repo`)
3. Click **"Analyze Repository"**
4. Wait for the analysis to complete
5. View the results in the dashboard

### Method 2: Upload Files

1. Click on the **"Upload Files"** tab
2. Click **"Choose Files"** and select your Python files
3. Click **"Upload & Analyze"**
4. Wait for the analysis to complete
5. View the results in the dashboard

## Understanding the Results

### Code Health Score
- **85-100**: Production Ready ✅
- **70-84**: Good
- **50-69**: Needs Improvement
- **0-49**: High Risk ⚠️

### Issue Severity Levels
- 🔴 **Critical**: Immediate attention required (security vulnerabilities)
- 🟠 **High**: Should be fixed soon (potential bugs, unsafe operations)
- 🟡 **Medium**: Should be addressed (code complexity, maintainability)
- 🟢 **Low**: Nice to have (documentation, minor improvements)

### Metrics Cards

1. **Files Analyzed**: Total number of Python files scanned
2. **Issues Found**: Total static code issues detected
3. **Security Findings**: Potential security vulnerabilities found

## Downloading Reports

After analysis completes, click the **"Download Full Report"** button to get a detailed markdown report including:
- Complete issue list
- watsonx.ai AI-powered recommendations
- IBM Bob IDE prompts for fixes
- Executive summary

## API Endpoints

The web UI exposes the following REST API endpoints:

### POST /api/analyze
Analyze a repository or uploaded files

**Request (Local Path):**
```json
{
  "repo_path": "./demo_repo"
}
```

**Request (File Upload):**
- Content-Type: multipart/form-data
- Field: files (multiple .py files)

**Response:**
```json
{
  "success": true,
  "data": {
    "files_analyzed": 2,
    "score": 85,
    "status": "Production Ready",
    "issues": [...],
    "mcp_findings": [...],
    "watsonx_summary": "...",
    "report_path": "outputs/devops_control_tower_report.md"
  }
}
```

### GET /api/report/<filename>
Download a generated report

### GET /health
Health check endpoint

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify `web_app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change port
```

### File Upload Issues
- Maximum file size: 16MB
- Only `.py` files are accepted
- Ensure files are valid Python code

### Analysis Errors
- Check that the repository path exists
- Ensure Python files are readable
- Verify watsonx.ai credentials if using AI features

## Security Considerations

⚠️ **Important Security Notes:**

1. **Production Deployment**: Change the Flask secret key in production
   ```python
   app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your-secure-key')
   ```

2. **File Upload**: The current implementation accepts file uploads. In production:
   - Add authentication
   - Implement rate limiting
   - Scan uploaded files for malware
   - Use a dedicated upload service

3. **HTTPS**: Always use HTTPS in production environments

4. **Environment Variables**: Never commit `.env` files with real credentials

## Development Mode

The web UI runs in debug mode by default for development. To run in production:

```python
# In web_app.py, change:
app.run(debug=False, host='0.0.0.0', port=5000)
```

Or use a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

## Customization

### Changing Colors
Edit the CSS variables in `templates/index.html`:
```css
:root {
    --primary-color: #0f62fe;  /* Change primary color */
    --success-color: #24a148;  /* Change success color */
    /* ... other colors */
}
```

### Adding Features
The Flask app is modular. Add new routes in `web_app.py` and corresponding UI in `templates/index.html`.

## Support

For issues or questions:
1. Check the main README.md
2. Review the WATSONX_SETUP_GUIDE.md for AI features
3. Check the demo_repo/REFACTORING_NOTES.md for code examples

---

**Built with ❤️ using Flask, IBM Carbon Design principles, and modern web technologies**