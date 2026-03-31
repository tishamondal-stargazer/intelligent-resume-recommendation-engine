# 🤖 Intelligent Resume Recommendation Engine

AI-powered web application that automatically matches resumes with job descriptions using **Natural Language Processing (NLP)** and **Similarity Learning**.

---

## 📋 Overview

In today's competitive job market, recruiters face the challenge of processing hundreds of resumes manually. This system automates candidate screening, reducing time from hours to milliseconds while eliminating bias and providing detailed skill analysis.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **Dual Matching Modes** | Basic (TF-IDF) and Advanced (Weighted Scoring) |
| **NLP Skill Extraction** | Identifies skills, experience, education from text |
| **Explainable AI** | Shows matched skills, missing skills, score breakdown |
| **Visual Analytics** | Bar charts and pie charts for easy interpretation |
| **Chatbot Assistant** | Answers questions about matching and resume tips |
| **Multiple Formats** | Supports PDF, DOCX, TXT files |
| **Real-time Processing** | <100ms per resume, no data stored |

---

## 🛠️ Technology Stack

| Category | Technologies |
|----------|--------------|
| **Backend** | Python, Flask |
| **NLP & ML** | NLTK, scikit-learn (TF-IDF, Cosine Similarity) |
| **File Parsing** | PyPDF2, python-docx |
| **Frontend** | HTML, CSS, JavaScript, Chart.js |

---

## 📊 Sample Results

Tested with job description for **"Senior Python Developer"**:

| Resume | Match Score | Recommendation |
|--------|-------------|----------------|
| Python Developer (5 yrs, Django, AWS) | **86.5%** | 🏆 Highly Suitable |
| Java Developer (4 yrs, basic Python) | **65.5%** | ✅ Good Fit |
| Fresher (basic Python, no experience) | **41.9%** | ⚠️ Moderate Fit |

---

## 📸 Screenshots

Screenshots of the working project are available in the **[screenshots](screenshots)** folder:

| # | Screenshot Name |
|---|-----------------|
| 1 | Homepage |
| 2 | Features Section |
| 3 | How It Works Section |
| 4 | AI Technology Stack |
| 5 | Job Description & File Upload |
| 6 | Basic Match Results |
| 7 | Advanced Match Results |
| 8 | Chatbot Assistant Interface |
| 9 | Login Modal |
| 10 | FAQ Section |
| 11 | Contact Form & Footer |

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.11 or higher
- Git (optional)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/tishamondal-stargazer/intelligent-resume-recommendation-engine.git
cd intelligent-resume-recommendation-engine

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate  # On Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# 5. Run the application
cd src
python app.py


Open browser: http://127.0.0.1:5000

📁 Project Structure
intelligent-resume-recommendation-engine/
├── src/
│   ├── app.py              # Flask web application
│   ├── parser.py           # PDF/DOCX/TXT parser
│   ├── matcher_basic.py    # Basic TF-IDF matching
│   └── matcher_advanced.py # Advanced weighted matching
├── templates/
│   └── index.html          # Frontend UI
├── data/
│   ├── resume1.txt         # Python Developer sample
│   ├── resume2.txt         # Java Developer sample
│   ├── resume3.txt         # Fresher sample
│   └── job_description.txt # Sample job description
├── screenshots/            # Project screenshots
├── requirements.txt        # Python dependencies
└── README.md              # This file

🔮 Future Enhancements
BERT integration for better context understanding

Multi-language support (Hindi, regional languages)

Resume builder with improvement suggestions

Mobile app version

👩‍💻 Author
Tisha Mondal
Computer Science Engineering Student | AI/ML Enthusiast

📧 Email: tishamondal128@gmail.com

🔗 LinkedIn: tisha-mondal-590535357

🐙 GitHub: tishamondal-stargazer


<div align="center"> Made with ❤️ by Tisha Mondal
⭐ If you found this project helpful, please give it a star!

</div> ```
