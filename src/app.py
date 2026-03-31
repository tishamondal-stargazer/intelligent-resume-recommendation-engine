"""
Intelligent Resume Recommendation Engine - Flask Web Application
Advanced version with graphical output support
"""

from flask import Flask, render_template, request, jsonify
import os
import tempfile
import json
from parser import DocumentParser
from matcher_basic import BasicResumeMatcher
from matcher_advanced import AdvancedResumeMatcher
import pandas as pd

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')

# Configure upload settings
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

# Initialize components
parser = DocumentParser()
basic_matcher = BasicResumeMatcher()
advanced_matcher = AdvancedResumeMatcher()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/match', methods=['POST'])
def match_resume():
    """Handle resume matching request"""
    try:
        # Get form data
        job_description = request.form.get('job_description', '')
        match_type = request.form.get('match_type', 'advanced')
        
        # Check if files were uploaded
        if 'resumes' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        files = request.files.getlist('resumes')
        
        if not files or files[0].filename == '':
            return jsonify({'error': 'No files selected'}), 400
        
        # Parse resumes
        resumes_text = []
        filenames = []
        
        for file in files:
            if file and allowed_file(file.filename):
                # Save temporarily
                temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(temp_path)
                
                # Parse resume
                resume_text = parser.parse_resume(temp_path)
                resumes_text.append(resume_text)
                filenames.append(file.filename)
                
                # Clean up
                os.remove(temp_path)
        
        if not resumes_text:
            return jsonify({'error': 'No valid resume files'}), 400
        
        # Perform matching based on type
        if match_type == 'basic':
            results_df = basic_matcher.calculate_similarity(job_description, resumes_text)
            results = []
            for idx, row in results_df.iterrows():
                results.append({
                    'Filename': filenames[int(row['Resume_Index'])],
                    'Resume_Index': int(row['Resume_Index']),
                    'Match_Score': float(row['Match_Score']),
                    'Status': row['Status']
                })
            
            summary = {
                'total_resumes': len(resumes_text),
                'average_score': round(results_df['Match_Score'].mean(), 2),
                'top_score': round(results_df['Match_Score'].max(), 2)
            }
        else:
            # Advanced match
            results_df = advanced_matcher.match_multiple_resumes(job_description, resumes_text)
            results = []
            for idx, row in results_df.iterrows():
                result = {
                    'Filename': filenames[int(row['Resume_ID']) - 1],
                    'Resume_ID': int(row['Resume_ID']),
                    'Total_Score': float(row['Total_Score']),
                    'Skills_Match': float(row['Skills_Match']),
                    'Experience_Match': float(row['Experience_Match']),
                    'Education_Match': float(row['Education_Match']),
                    'Matching_Skills': row['Matching_Skills'] if 'Matching_Skills' in row else '',
                    'Missing_Skills': row['Missing_Skills'] if 'Missing_Skills' in row else '',
                    'Recommendation': row['Recommendation'] if 'Recommendation' in row else row['Fit_Level']
                }
                results.append(result)
            
            summary = {
                'total_resumes': len(resumes_text),
                'average_score': round(results_df['Total_Score'].mean(), 2),
                'top_score': round(results_df['Total_Score'].max(), 2)
            }
        
        return jsonify({
            'success': True,
            'match_type': match_type,
            'results': results,
            'summary': summary
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze_single():
    """Analyze single resume in detail"""
    try:
        job_description = request.form.get('job_description', '')
        
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume uploaded'}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(temp_path)
            
            resume_text = parser.parse_resume(temp_path)
            
            if request.form.get('analysis_type', 'basic') == 'basic':
                result = basic_matcher.get_matching_details(job_description, resume_text)
            else:
                result = advanced_matcher.calculate_comprehensive_match(job_description, resume_text)
            
            os.remove(temp_path)
            
            return jsonify({
                'success': True,
                'filename': file.filename,
                'analysis': result
            })
        
        return jsonify({'error': 'Invalid file type'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('../templates', exist_ok=True)
    os.makedirs('../static', exist_ok=True)
    
    # Run the app
    app.run(debug=True, host='127.0.0.1', port=5000)