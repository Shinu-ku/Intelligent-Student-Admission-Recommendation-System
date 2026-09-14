# Intelligent Student Admission Recommendation System

An AI-powered university admission decision-support platform that automates application intake, document OCR verification, rule-based eligibility evaluation, and machine learning suitability scoring with Explainable AI (XAI), while keeping final admission decisions strictly under human control (**Human-in-the-Loop**).

---

## 🌟 Key Features

### 🎓 Student Portal
- **User Authentication**: Secure student registration and session-based authentication.
- **5-Step Application Form**: Personal Info, Academic Marks, Course Branch Selection (B.Tech CSE, IT, ECE, ME, EE), Additional Info (Olympiads, Certifications, Work Experience), and Review.
- **Document Management & OCR Audit**: Upload Class 10 & 12 marksheets, entrance scorecards, and ID proofs. Processed via OpenCV + Pytesseract OCR pipeline with graceful fallback to a labeled Demo OCR simulation mode.
- **DigiLocker Simulation**: Realistic prototype integration showing authentic verified badges.
- **Rule-Based Eligibility Engine**: Transparent pass/fail rule breakdown based on selected course criteria.
- **AI Suitability Score & XAI**: Scikit-Learn Random Forest model scoring (0–100%) and feature importance visualization highlighting positive factors and potential concerns.
- **7-Step Status Tracker Bar**: Live progression tracking from Submission to Final Admission Officer Decision.

### 🛡️ Admission Officer Portal (Command Center)
- **Command Center Dashboard**: Live metric counters for total applications, pending reviews, eligible applicants, AI recommended candidates, and final decisions.
- **Directory & Multi-Filter Table**: Instant text search and multi-filtering by course, eligibility status, AI recommendation category, and officer decision.
- **360° Candidate Profile**: Comprehensive overview containing academic marks, OCR document audit, eligibility checks, AI score, XAI chart, and decision panel.
- **Human-in-the-Loop Decision & Override**: Officers can record Accept, Reject, or Hold decisions with written comments. Supports and tracks explicit human overrides against AI recommendations.
- **Visual Analytics**: Interactive Chart.js graphs displaying Applications by Course, Eligibility Distribution, AI Recommendation Breakdown, and Processing Funnel.
- **AI Model Transparency**: Detailed ML performance metrics (Accuracy, Precision, Recall, F1 Score) and synthetic dataset disclaimers.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.11, Flask, SQLite3, Werkzeug Security
- **Machine Learning**: Scikit-Learn (`RandomForestClassifier`), Pandas, NumPy, Joblib
- **Document Processing**: OpenCV (`opencv-python-headless`), Pytesseract OCR, Pillow
- **Frontend**: HTML5, CSS3, JavaScript (ES6), Bootstrap 5, FontAwesome 6, Chart.js

---

## 🚀 Installation & Setup Instructions

### 1. Prerequisites
Ensure Python 3.9+ is installed on your system.

### 2. Clone / Navigate to Directory
```bash
cd d:/programming/Projects/AI_PBL
```

### 3. Set Up Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ⚙️ Model Training & Database Seeding

### 1. Train Random Forest ML Model
Generate the synthetic dataset (1,000 records) and train the Random Forest model:
```bash
python ml/train_model.py
```
*Outputs: `ml/dataset.csv`, `ml/model.pkl`, `ml/scaler.pkl`, and `ml/metrics.pkl`.*

### 2. Initialize & Seed Database
Initialize SQLite tables and populate 25+ realistic applicant profiles:
```bash
python seed_data.py
```

---

## 🔑 Demo Credentials

| Role | Email | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Admission Officer** | `admin@university.edu` | `admin123` | Full Admin Command Center |
| **Student Demo** | `soumya@example.com` | `student123` | Student Portal & Application |

---

## 🏃 Running the Application

Start the Flask web server:
```bash
python app.py
```

Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 📁 Project Structure

```text
AI_PBL/
├── app.py                      # Flask main app entry point
├── config.py                   # App configuration & session settings
├── database/
│   ├── db.py                   # SQLite database helper wrapper
│   ├── schema.sql              # Relational database schema
│   └── admission_system.db     # SQLite database file
├── models/
│   ├── user.py                 # User authentication model
│   ├── application.py          # Application entity & status model
│   ├── document.py             # Document & OCR records model
│   └── ai_info.py              # AI score & XAI persistence model
├── routes/
│   ├── auth.py                 # Authentication routes (Login/Register)
│   ├── student.py              # Student dashboard routes
│   ├── application.py          # 5-step application wizard routes
│   ├── documents.py            # Upload, OCR, & DigiLocker simulation
│   ├── eligibility.py          # Rule-based eligibility routes
│   ├── ai.py                   # AI recommendation & XAI routes
│   └── admin.py                # Admission officer command center routes
├── services/
│   ├── ocr_service.py          # OpenCV + Pytesseract OCR service
│   ├── eligibility_engine.py   # Course-wise eligibility rule engine
│   ├── recommendation_engine.py# Random Forest suitability prediction
│   └── explainability.py       # XAI feature importance & narratives
├── ml/
│   ├── dataset_generator.py    # Synthetic dataset creation
│   ├── train_model.py          # Model training & metrics script
│   ├── dataset.csv             # Generated synthetic dataset
│   ├── model.pkl               # Trained Random Forest artifact
│   └── scaler.pkl              # Feature scaling artifact
├── static/
│   ├── css/style.css           # Premium dark theme stylesheet
│   └── js/
│       ├── main.js             # Form wizard & DigiLocker AJAX
│       └── charts.js           # Chart.js visualization helpers
├── templates/                  # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── student/
│   └── admin/
├── uploads/                    # Local storage for marksheets
├── seed_data.py                # Seed script for 25+ demo applicants
├── requirements.txt            # Python dependencies
└── README.md                   # System documentation
```

---

## ⚠️ Known Limitations & Disclaimer

> **Academic Prototype Disclaimer**: This machine learning model is trained using synthetic demonstration data (1,000 records). Its predictions should not be used for real university admission decisions.
> 
> **OCR & DigiLocker**: The OCR pipeline uses OpenCV & Pytesseract. If Tesseract binary is not installed on system PATH, the application automatically switches to a labeled Demo OCR Simulation mode to allow seamless evaluation. DigiLocker integration is implemented as an interactive prototype simulation as specified in academic requirements.
