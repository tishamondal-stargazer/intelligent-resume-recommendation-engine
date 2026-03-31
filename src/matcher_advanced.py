"""
Enhanced Advanced Resume Matcher with Explainable AI
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from parser import DocumentParser
import json

class AdvancedResumeMatcher:
    """Enhanced resume matching with explainable AI"""
    
    # Job role templates for recommendation
    JOB_ROLES = {
        'python': ['Python Developer', 'Backend Engineer', 'Software Engineer', 'Data Engineer'],
        'java': ['Java Developer', 'Backend Engineer', 'Software Engineer', 'Android Developer'],
        'javascript': ['Frontend Developer', 'Full Stack Developer', 'React Developer', 'Web Developer'],
        'machine learning': ['ML Engineer', 'Data Scientist', 'AI Engineer', 'NLP Engineer'],
        'data science': ['Data Scientist', 'Data Analyst', 'ML Engineer', 'Business Analyst'],
        'devops': ['DevOps Engineer', 'Cloud Engineer', 'SRE', 'Platform Engineer']
    }
    
    def __init__(self, skill_weights=None):
        self.parser = DocumentParser()
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
        self.skill_weights = skill_weights or {
            'python': 0.9, 'java': 0.8, 'javascript': 0.8,
            'react': 0.7, 'angular': 0.7, 'node.js': 0.7,
            'aws': 0.6, 'docker': 0.6, 'kubernetes': 0.6,
            'machine learning': 0.9, 'deep learning': 0.9,
            'sql': 0.7, 'nosql': 0.6,
            'communication': 0.4, 'leadership': 0.5,
            'agile': 0.4, 'project management': 0.5
        }
        
        self.component_weights = {
            'skills_match': 0.5,
            'experience_match': 0.2,
            'education_match': 0.15,
            'text_similarity': 0.15
        }
    
    def calculate_skills_match(self, job_skills: list, resume_skills: list) -> tuple:
        """Calculate weighted skills match score with details"""
        if not job_skills:
            return 0.0, [], []
        
        job_skills_set = set([s.lower() for s in job_skills])
        resume_skills_set = set([s.lower() for s in resume_skills])
        
        matched_skills = list(job_skills_set & resume_skills_set)
        missing_skills = list(job_skills_set - resume_skills_set)
        
        total_weight = 0
        matched_weight = 0
        
        for skill in job_skills_set:
            weight = self.skill_weights.get(skill.lower(), 0.5)
            total_weight += weight
            if skill in resume_skills_set:
                matched_weight += weight
        
        if total_weight > 0:
            base_score = (matched_weight / total_weight) * 100
            return base_score, matched_skills, missing_skills
        return 0.0, [], []
    
    def calculate_experience_match(self, job_exp: float, resume_exp: float) -> tuple:
        """Calculate experience match with explanation"""
        if job_exp == 0:
            return 100.0, "No experience requirement specified"
        
        if resume_exp >= job_exp:
            ratio = job_exp / resume_exp
            score = min(ratio * 100, 100)
            if resume_exp > job_exp * 1.5:
                explanation = f"Candidate has {resume_exp} years (more than required) - Good but might be overqualified"
            else:
                explanation = f"Candidate has {resume_exp} years (meets requirement of {job_exp} years)"
        else:
            ratio = resume_exp / job_exp
            score = ratio * 100
            explanation = f"Candidate has {resume_exp} years (short of {job_exp} years required)"
        
        return score, explanation
    
    def calculate_education_match(self, job_edu_level: int, resume_edu_level: int) -> tuple:
        """Calculate education match with explanation"""
        if job_edu_level == 0:
            return 100.0, "No education requirement specified"
        
        edu_levels = {1: "High School", 2: "Diploma", 3: "Bachelor's", 4: "Master's", 5: "PhD"}
        
        if resume_edu_level >= job_edu_level:
            score = 100.0
            explanation = f"Candidate has {edu_levels.get(resume_edu_level, 'Degree')} (meets requirement of {edu_levels.get(job_edu_level, 'Degree')})"
        else:
            score = (resume_edu_level / job_edu_level) * 100
            explanation = f"Candidate has {edu_levels.get(resume_edu_level, 'Degree')} (needs {edu_levels.get(job_edu_level, 'Degree')})"
        
        return score, explanation
    
    def recommend_job_roles(self, skills: list) -> list:
        """Recommend job roles based on skills"""
        recommendations = set()
        skills_lower = [s.lower() for s in skills]
        
        for key, roles in self.JOB_ROLES.items():
            if key in str(skills_lower):
                for role in roles:
                    recommendations.add(role)
        
        if not recommendations:
            recommendations.add("General Software Developer")
            recommendations.add("IT Professional")
        
        return list(recommendations)[:5]
    
    def generate_improvement_tips(self, missing_skills: list, ats_score: dict) -> list:
        """Generate resume improvement tips"""
        tips = []
        
        if missing_skills:
            tips.append(f"💡 Add these missing skills: {', '.join(missing_skills[:3])}")
        
        for reason in ats_score.get('reasons', []):
            if reason.startswith('✗'):
                tips.append(f"💡 {reason[2:]}")
        
        tips.append("💡 Use action verbs like 'Developed', 'Led', 'Implemented'")
        tips.append("💡 Add quantifiable achievements (e.g., 'Improved by 20%')")
        
        return tips[:5]
    
    def calculate_comprehensive_match(self, job_desc: str, resume_text: str) -> dict:
        """Calculate comprehensive match with explainable AI"""
        
        # Extract features
        job_skills = self.parser.get_flat_skills(job_desc)
        resume_skills = self.parser.get_flat_skills(resume_text)
        
        job_exp = self.parser.extract_experience(job_desc)
        resume_exp = self.parser.extract_experience(resume_text)
        
        job_edu, job_edu_level = self.parser.extract_education(job_desc)
        resume_edu, resume_edu_level = self.parser.extract_education(resume_text)
        
        # Calculate individual scores with explanations
        skills_score, matched_skills, missing_skills = self.calculate_skills_match(job_skills, resume_skills)
        exp_score, exp_explanation = self.calculate_experience_match(job_exp, resume_exp)
        edu_score, edu_explanation = self.calculate_education_match(job_edu_level, resume_edu_level)
        
        # Calculate text similarity
        vectors = self.vectorizer.fit_transform([job_desc, resume_text])
        text_similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0] * 100
        
        # Calculate weighted total
        total_score = (
            self.component_weights['skills_match'] * skills_score +
            self.component_weights['experience_match'] * exp_score +
            self.component_weights['education_match'] * edu_score +
            self.component_weights['text_similarity'] * text_similarity
        )
        
        # Determine fit level
        if total_score >= 80:
            fit_level = "Highly Suitable"
            fit_color = "#28a745"
        elif total_score >= 60:
            fit_level = "Good Fit"
            fit_color = "#17a2b8"
        elif total_score >= 40:
            fit_level = "Moderate Fit"
            fit_color = "#ffc107"
        else:
            fit_level = "Low Fit"
            fit_color = "#dc3545"
        
        # Calculate ATS score
        ats_result = self.parser.calculate_ats_score(resume_text)
        
        # Generate recommendations
        recommended_roles = self.recommend_job_roles(resume_skills)
        improvement_tips = self.generate_improvement_tips(missing_skills, ats_result)
        
        # Build score breakdown for explainable AI
        score_breakdown = {
            'skills': {'score': skills_score, 'weight': self.component_weights['skills_match'] * 100, 'contribution': (skills_score * self.component_weights['skills_match'])},
            'experience': {'score': exp_score, 'weight': self.component_weights['experience_match'] * 100, 'contribution': (exp_score * self.component_weights['experience_match'])},
            'education': {'score': edu_score, 'weight': self.component_weights['education_match'] * 100, 'contribution': (edu_score * self.component_weights['education_match'])},
            'text_similarity': {'score': text_similarity, 'weight': self.component_weights['text_similarity'] * 100, 'contribution': (text_similarity * self.component_weights['text_similarity'])}
        }
        
        return {
            'total_score': round(total_score, 2),
            'fit_level': fit_level,
            'fit_color': fit_color,
            'skills_match': round(skills_score, 2),
            'experience_match': round(exp_score, 2),
            'education_match': round(edu_score, 2),
            'text_similarity': round(text_similarity, 2),
            'matching_skills': matched_skills,
            'missing_skills': missing_skills,
            'job_experience_required': job_exp,
            'candidate_experience': resume_exp,
            'exp_explanation': exp_explanation,
            'edu_explanation': edu_explanation,
            'ats_score': ats_result['score'],
            'ats_feedback': ats_result['reasons'],
            'recommended_roles': recommended_roles,
            'improvement_tips': improvement_tips,
            'score_breakdown': score_breakdown
        }
    
    def match_multiple_resumes(self, job_desc: str, resumes: list) -> pd.DataFrame:
        """Match job with multiple resumes"""
        results = []
        
        for i, resume in enumerate(resumes):
            match_result = self.calculate_comprehensive_match(job_desc, resume)
            results.append({
                'Resume_ID': i + 1,
                'Total_Score': match_result['total_score'],
                'Fit_Level': match_result['fit_level'],
                'Skills_Match': match_result['skills_match'],
                'Experience_Match': match_result['experience_match'],
                'Education_Match': match_result['education_match'],
                'ATS_Score': match_result['ats_score'],
                'Matching_Skills': ', '.join(match_result['matching_skills'][:5]),
                'Missing_Skills': ', '.join(match_result['missing_skills'][:5]),
                'Recommendation': match_result['fit_level']
            })
        
        df = pd.DataFrame(results)
        return df.sort_values('Total_Score', ascending=False)