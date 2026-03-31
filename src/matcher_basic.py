"""
Basic Resume Matcher using TF-IDF and Cosine Similarity
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import warnings
warnings.filterwarnings('ignore')

class BasicResumeMatcher:
    """Basic resume matching using TF-IDF"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            lowercase=True
        )
        self.is_fitted = False
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('english'))
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text"""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        text = ' '.join(text.split())
        words = word_tokenize(text)
        words = [w for w in words if w not in self.stop_words and len(w) > 2]
        return ' '.join(words)
    
    def prepare_documents(self, job_desc: str, resumes: list) -> tuple:
        """Prepare job and resume documents for matching"""
        job_processed = self.preprocess_text(job_desc)
        resumes_processed = [self.preprocess_text(resume) for resume in resumes]
        all_docs = [job_processed] + resumes_processed
        return all_docs, job_processed, resumes_processed
    
    def calculate_similarity(self, job_desc: str, resumes: list) -> pd.DataFrame:
        """Calculate similarity between job and all resumes"""
        
        all_docs, job_processed, resumes_processed = self.prepare_documents(job_desc, resumes)
        
        tfidf_matrix = self.vectorizer.fit_transform(all_docs)
        self.is_fitted = True
        
        job_vector = tfidf_matrix[0:1]
        resume_vectors = tfidf_matrix[1:]
        
        similarities = cosine_similarity(job_vector, resume_vectors).flatten()
        
        # LOWERED THRESHOLDS for better acceptance
        results = pd.DataFrame({
            'Resume_Index': range(len(resumes)),
            'Match_Score': similarities * 100,
            'Status': ['Match' if score > 20 else 'Review' if score > 10 else 'Reject' 
                      for score in similarities * 100]
        })
        
        return results.sort_values('Match_Score', ascending=False)
    
    def get_matching_details(self, job_desc: str, resume_text: str) -> dict:
        """Get detailed matching information for a single resume"""
        
        job_processed = self.preprocess_text(job_desc)
        resume_processed = self.preprocess_text(resume_text)
        
        tfidf_matrix = self.vectorizer.fit_transform([job_processed, resume_processed])
        
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        feature_names = self.vectorizer.get_feature_names_out()
        job_vector = tfidf_matrix[0].toarray()[0]
        resume_vector = tfidf_matrix[1].toarray()[0]
        
        job_top_indices = job_vector.argsort()[-10:][::-1]
        resume_top_indices = resume_vector.argsort()[-10:][::-1]
        
        job_top_terms = [feature_names[i] for i in job_top_indices if job_vector[i] > 0]
        resume_top_terms = [feature_names[i] for i in resume_top_indices if resume_vector[i] > 0]
        
        common_terms = set(job_top_terms) & set(resume_top_terms)
        
        # LOWERED THRESHOLDS for recommendation
        if similarity > 0.25:
            recommendation = 'Strong Match'
        elif similarity > 0.15:
            recommendation = 'Potential Match'
        else:
            recommendation = 'Weak Match'
        
        return {
            'match_score': similarity * 100,
            'job_key_terms': job_top_terms[:5],
            'resume_key_terms': resume_top_terms[:5],
            'common_terms': list(common_terms),
            'recommendation': recommendation
        }


if __name__ == "__main__":
    matcher = BasicResumeMatcher()
    
    job = """
    We are looking for a Python Developer with 3+ years of experience.
    Required skills: Python, Django, REST APIs, SQL, Git.
    """
    
    resumes = [
        """
        Experienced Python developer with 4 years in web development.
        Proficient in Django, Flask, and REST APIs.
        Strong SQL and database design skills.
        """,
        
        """
        Java developer with 5 years experience in enterprise applications.
        Skilled in Spring Boot, Hibernate, and Oracle database.
        """
    ]
    
    results = matcher.calculate_similarity(job, resumes)
    print("\n=== Matching Results ===")
    print(results)