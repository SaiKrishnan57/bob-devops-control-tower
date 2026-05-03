"""
Bob DevOps Control Tower - Web Interface
A modern web UI for code analysis and health monitoring
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import shutil
from pathlib import Path
from datetime import datetime
from app.pipeline import run_pipeline

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)


@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_repository():
    """
    API endpoint to analyze a repository.
    Accepts either a local path or uploaded files.
    """
    try:
        # Check if it's a path or file upload
        if 'repo_path' in request.form:
            repo_path = request.form['repo_path']
            
            if not os.path.exists(repo_path):
                return jsonify({
                    'success': False,
                    'error': f'Repository path does not exist: {repo_path}'
                }), 400
            
        elif 'files' in request.files:
            # Handle file upload
            files = request.files.getlist('files')
            
            if not files or files[0].filename == '':
                return jsonify({
                    'success': False,
                    'error': 'No files selected'
                }), 400
            
            # Create temporary directory for uploaded files
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            repo_path = os.path.join(app.config['UPLOAD_FOLDER'], f'repo_{timestamp}')
            os.makedirs(repo_path, exist_ok=True)
            
            # Save uploaded files
            for file in files:
                if file and file.filename.endswith('.py'):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(repo_path, filename))
        else:
            return jsonify({
                'success': False,
                'error': 'No repository path or files provided'
            }), 400
        
        # Run the analysis pipeline
        result = run_pipeline(repo_path)
        
        # Clean up uploaded files if they were temporary
        if 'files' in request.files:
            shutil.rmtree(repo_path, ignore_errors=True)
        
        return jsonify({
            'success': True,
            'data': {
                'files_analyzed': result['files_analyzed'],
                'score': result['score']['score'],
                'status': result['score']['status'],
                'issues': result['issues'],
                'mcp_findings': result['mcp_findings'],
                'watsonx_summary': result['watsonx_summary'],
                'report_path': result['report_path']
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/report/<path:filename>')
def download_report(filename):
    """Download the generated markdown report."""
    try:
        report_path = os.path.join('outputs', filename)
        if os.path.exists(report_path):
            return send_file(report_path, as_attachment=True)
        else:
            return jsonify({
                'success': False,
                'error': 'Report not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    print("\n" + "="*50)
    print("Bob DevOps Control Tower - Web Interface")
    print("="*50)
    print("\nStarting server at http://localhost:5000")
    print("Press CTRL+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob
