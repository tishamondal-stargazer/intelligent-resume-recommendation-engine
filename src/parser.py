"""
Enhanced Document Parser with More Skills Extraction
"""

import PyPDF2
import docx
import re
import os
from typing import List, Dict, Tuple

class DocumentParser:
    """Parse different document formats and extract text"""
    
    # Expanded skill database
    SKILL_DATABASE = {
        'programming_languages': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'go', 'rust', 'swift', 'kotlin', 'typescript', 'scala', 'perl', 'r', 'matlab'],
        'web_frameworks': ['django', 'flask', 'react', 'angular', 'vue', 'node.js', 'express', 'spring', 'spring boot', 'asp.net', 'laravel', 'ruby on rails'],
        'databases': ['sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'sqlite', 'dynamodb', 'cassandra', 'redis', 'elasticsearch'],
        'cloud_platforms': ['aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean', 'cloudfoundry'],
        'devops_tools': ['docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab', 'bitbucket', 'ci/cd', 'ansible', 'terraform', 'prometheus', 'grafana'],
        'ai_ml': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'nlp', 'computer vision', 'llm', 'gpt', 'bert', 'transformers', 'pandas', 'numpy'],
        'soft_skills': ['communication', 'leadership', 'teamwork', 'problem solving', 'critical thinking', 'time management', 'project management', 'agile', 'scrum'],
        'certifications': ['aws certified', 'azure certified', 'gcp certified', 'pmp', 'scrum master', 'data science certified']
    }
    
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + " "
            return text.strip()
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            return ""
    
    @staticmethod
    def extract_text_from_docx(docx_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(docx_path)
            text = " ".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            print(f"Error reading DOCX {docx_path}: {e}")
            return ""
    
    @staticmethod
    def read_text_file(txt_path: str) -> str:
        """Read text from TXT file"""
        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            print(f"Error reading TXT {txt_path}: {e}")
            return ""
    
    def parse_resume(self, file_path: str) -> str:
        """Parse resume based on file extension"""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif ext == '.docx':
            return self.extract_text_from_docx(file_path)
        elif ext == '.txt':
            return self.read_text_file(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    
    def extract_all_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract skills by category"""
        text_lower = text.lower()
        found_skills = {}
        
        for category, skills in self.SKILL_DATABASE.items():
            found = []
            for skill in skills:
                if skill.lower() in text_lower:
                    found.append(skill)
            if found:
                found_skills[category] = found
        
        return found_skills
    
    def get_flat_skills(self, text: str) -> List[str]:
        """Get flat list of all skills found"""
        skills_dict = self.extract_all_skills(text)
        flat_skills = []
        for skills in skills_dict.values():
            flat_skills.extend(skills)
        return flat_skills
    
    def extract_experience(self, text: str) -> float:
        """Extract years of experience from text"""
        patterns = [
            r'(\d+)\+?\s*years?.*?experience',
            r'experience.*?(\d+)\+?\s*years?',
            r'(\d+)\s*yr?s?',
            r'(\d+)\+?\s*years?.*?of.*?experience'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                try:
                    return float(matches[0])
                except:
                    pass
        return 0.0
    
    def extract_education(self, text: str) -> List[str]:
        """Extract education information with levels"""
        education_keywords = {
            'phd': ['phd', 'doctorate', 'doctor of philosophy'],
            'masters': ['master', 'm.tech', 'm.e.', 'm.sc', 'mba', 'ms', 'm.s.'],
            'bachelors': ['bachelor', 'b.tech', 'b.e.', 'b.sc', 'ba', 'b.a.', 'b.com', 'b.b.a'],
            'diploma': ['diploma', 'polytechnic'],
            'high_school': ['high school', '12th', 'hsc', 'intermediate']
        }
        
        text_lower = text.lower()
        found_education = []
        education_level = 0
        
        for level, keywords in education_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_education.append(f"{level.replace('_', ' ').title()}: {keyword.title()}")
                    if level == 'phd':
                        education_level = 5
                    elif level == 'masters':
                        education_level = max(education_level, 4)
                    elif level == 'bachelors':
                        education_level = max(education_level, 3)
                    elif level == 'diploma':
                        education_level = max(education_level, 2)
                    elif level == 'high_school':
                        education_level = max(education_level, 1)
                    break
        
        return found_education, education_level
    
    def calculate_ats_score(self, text: str) -> Dict:
        """Calculate ATS compatibility score"""
        text_lower = text.lower()
        score = 0
        max_score = 100
        reasons = []
        
        # Check for contact information
        if re.search(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', text):
            score += 15
            reasons.append("✓ Email address found")
        else:
            reasons.append("✗ Missing email address")
        
        # Check for phone number
        if re.search(r'\b\d{10}\b|\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text):
            score += 15
            reasons.append("✓ Phone number found")
        else:
            reasons.append("✗ Missing phone number")
        
        # Check for LinkedIn/GitHub
        if 'linkedin' in text_lower or 'github' in text_lower:
            score += 10
            reasons.append("✓ Professional profile link found")
        else:
            reasons.append("✗ Consider adding LinkedIn/GitHub profile")
        
        # Check for action verbs
        action_verbs = ['developed', 'created', 'managed', 'led', 'implemented', 'designed', 'built', 'improved']
        verb_count = sum(1 for verb in action_verbs if verb in text_lower)
        if verb_count >= 3:
            score += 20
            reasons.append(f"✓ Good use of action verbs ({verb_count} found)")
        else:
            reasons.append(f"✗ Use more action verbs (only {verb_count} found)")
        
        # Check for quantifiable achievements
        if re.search(r'\d+%|\d+\s*(percent|%)\s*(increase|improve|reduce)', text_lower):
            score += 20
            reasons.append("✓ Quantifiable achievements found")
        else:
            reasons.append("✗ Add quantifiable achievements (e.g., 'Improved by 20%')")
        
        # Check for skills section
        if 'skills' in text_lower or 'technologies' in text_lower:
            score += 20
            reasons.append("✓ Clear skills section found")
        else:
            reasons.append("✗ Add a dedicated skills section")
        
        return {
            'score': min(score, max_score),
            'max_score': max_score,
            'reasons': reasons
        }