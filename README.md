# 🎓 University Admission Recommendation System

A **Flask-based Machine Learning web app** that recommends suitable **universities** based on a student’s academic marks, fee affordability, and interests.  
It also predicts **future career paths** for the chosen department using **Google Gemini (Generative AI)**.

---

## 🚀 Project Overview

This system helps students make informed university choices through data-driven predictions and AI-powered insights.  
It combines a trained **scikit-learn model** with **Gemini AI** to generate practical career suggestions for each department.

### 🔹 How It Works
1. User registers or logs in (Flask authentication system).  
2. User enters:
   - HSSC Marks (%)
   - SSC Marks (%)
   - Affordable Fee
   - Department / Area of Interest
3. The ML model predicts the **most suitable university**.
4. Gemini AI suggests **three future career options** based on the selected department.

---

## 🧱 Tech Stack

| Category | Technologies |
|-----------|---------------|
| Backend | Flask, Flask-WTF, Flask-Login, Flask-Migrate, Flask-SQLAlchemy |
| Frontend | HTML, CSS (Bootstrap), Jinja2 Templates |
| Machine Learning | scikit-learn, pandas, numpy |
| AI Integration | Google Gemini via `google-generativeai` |
| Others | Python-dotenv, SQLite, Joblib, Werkzeug |

---

## 📂 Project Structure 

university-recommender-system/

│

├── app.py # Main Flask application

├── future_prediction.py # Gemini-based career suggestion module

├── final_model.pkl # Trained ML model
│
├── requirements.txt

├── .gitignore

├── .env.example

├── README.md

│

├── templates/ # HTML templates

│ ├── index.html

│ ├── login.html

│ ├── signup.html

│ └── dashboard.html

│
├── static/ # CSS / JS / Images

│ └── style.css

│

├── migrations/ # Database migrations (Flask-Migrate)

├── assets/ # Screenshots for GitHub

│ ├── home.png

│ └── results.png

│

├── instance/ # Local runtime database (ignored)

├── pycache/ # Cached files (ignored)

└── .venv/ # Virtual environment (ignored) 


## 📂 Screen Shots: 


<img width="1002" height="668" alt="Screenshot 2025-10-22 023327" src="https://github.com/user-attachments/assets/859b41cd-d222-4bf7-8ae2-1bdd2136b1be" /> 

<img width="1483" height="686" alt="Screenshot 2025-10-22 023342" src="https://github.com/user-attachments/assets/4d354f88-fbc6-4ad7-8dff-7d0480ef52f0" />

