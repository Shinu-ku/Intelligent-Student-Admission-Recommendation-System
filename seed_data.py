import json
import random
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from config import Config
from database.db import init_db, execute_db, query_db
from models.user import User
from models.application import Application
from models.document import DocumentModel
from models.ai_info import AIInfo
from services.eligibility_engine import evaluate_eligibility
from services.recommendation_engine import predict_admission_suitability
from services.explainability import generate_explainability

COURSES = [
    'B.Tech Computer Science & Engineering',
    'B.Tech Information Technology',
    'B.Tech Electronics & Communication',
    'B.Tech Mechanical Engineering',
    'B.Tech Electrical Engineering'
]

NAMES = [
    "Soumya Kushwah", "Dhruv Agarwal", "Sachin Dixit", "Ananya Sharma", "Rohan Mehta",
    "Priya Verma", "Aarav Patel", "Isha Gupta", "Kabir Singh", "Neha Joshi",
    "Vikram Reddy", "Siddharth Rao", "Kavya Nair", "Aditya Kapoor", "Tanvi Bhatia",
    "Manish Kumar", "Pooja Roy", "Rajesh Pillai", "Simran Kaur", "Harsh Vardhan",
    "Ritu Choudhary", "Gaurav Malhotra", "Sneha Das", "Rahul Saxena", "Meera Iyer"
]

def seed_database():
    print("Initializing Database Schema...")
    init_db()
    
    # 1. Create Accounts
    print("Creating Demo User Accounts...")
    admin_id = User.create("Senior Admission Officer", "admin@university.edu", "admin123", role="admin", phone="+91 98765 43210")
    soumya_id = User.create("Soumya Kushwah", "soumya@example.com", "student123", role="student", phone="+91 91234 56789", dob="2005-04-12")
    
    # 2. Seed Demo Scenario for Soumya (B.Tech CSE, 89% Class 12, 82 Entrance)
    print("Seeding Soumya Kushwah's Application...")
    app_id, app_num = Application.create(soumya_id, "B.Tech Computer Science & Engineering")
    Application.save_academic_info(app_id, {
        'class10_percentage': 92.0,
        'class12_percentage': 89.0,
        'mathematics': 91.0,
        'physics': 87.0,
        'chemistry': 89.0,
        'entrance_exam': 'JEE Main',
        'entrance_score': 82.0,
        'passing_year': 2025,
        'school_board': 'CBSE',
        'achievements': 'State Level Math Olympiad Gold Medalist\nNational Cyber Challenge Top 10',
        'certifications': 'Python for Data Science (Coursera)\nAWS Cloud Fundamentals',
        'extracurricular': 'Tech Club President, Debate Team Captain',
        'work_experience': 'Summer Coding Intern at TechStart',
        'sop': 'Driven to pursue B.Tech CSE to focus on Artificial Intelligence and Scalable Machine Learning systems.'
    })
    
    # Add Documents for Soumya
    DocumentModel.add(app_id, "Class 10 Marksheet", "uploads/demo_class10.pdf", "soumya_class10.pdf", "CBSE CLASS X MARKSHEET - Soumya Kushwah - CGPA 9.6", "VERIFIED", "OCR Match 100%")
    DocumentModel.add(app_id, "Class 12 Marksheet", "uploads/demo_class12.pdf", "soumya_class12.pdf", "CBSE CLASS XII MARKSHEET - Soumya Kushwah - Maths: 91, Phys: 87, Chem: 89, Agg: 89.0%", "VERIFIED", "OCR Match 100%")
    DocumentModel.add(app_id, "Entrance Scorecard", "uploads/demo_entrance.pdf", "soumya_jee.pdf", "JEE MAIN SCORECARD - Soumya Kushwah - Score: 82.0", "VERIFIED", "Verified via NTA Database", is_digilocker=1)
    DocumentModel.add(app_id, "Identity Proof", "uploads/demo_id.pdf", "soumya_aadhaar.pdf", "GOVT OF INDIA - AADHAAR CARD - Soumya Kushwah", "VERIFIED", "DigiLocker Authenticated", is_digilocker=1)
    DocumentModel.add(app_id, "Passport Photograph", "uploads/demo_photo.jpg", "soumya_photo.jpg", "PASSPORT PHOTO - Soumya Kushwah", "VERIFIED", "Biometric Format Valid")
    
    # Eligibility & AI for Soumya
    _, elig_summary = evaluate_eligibility("B.Tech Computer Science & Engineering", {
        'class12_percentage': 89.0, 'mathematics': 91.0, 'physics': 87.0, 'chemistry': 89.0, 'entrance_score': 82.0, 'entrance_exam': 'JEE Main'
    })
    execute_db("INSERT INTO eligibility_results (application_id, is_eligible, summary_json) VALUES (?, 1, ?)", (app_id, json.dumps(elig_summary)))
    
    pred = predict_admission_suitability({
        'class10_percentage': 92.0, 'class12_percentage': 89.0, 'mathematics': 91.0, 'physics': 87.0,
        'chemistry': 89.0, 'entrance_score': 82.0, 'achievements': 2, 'certifications': 2, 'extracurricular': 'President'
    })
    xai = generate_explainability(pred['feature_dict'], pred['suitability_score'], "B.Tech Computer Science & Engineering")
    AIInfo.save(app_id, pred['suitability_score'], pred['recommendation'], xai['feature_importance'], xai)
    Application.update_status(app_id, 'OFFICER_REVIEW')
    
    # 3. Seed 24 Additional Realistic Applicants
    print("Seeding 24 Additional Applicant Records...")
    random.seed(101)
    
    for i in range(1, 25):
        name = NAMES[i]
        email = f"student{i}@example.com"
        course = random.choice(COURSES)
        
        # Student user account
        u_id = User.create(name, email, "student123", role="student", phone=f"+91 98765 {10000+i}")
        a_id, a_num = Application.create(u_id, course)
        
        # Varied candidate profiles: Strong, Average, Borderline, Ineligible
        profile_type = i % 4
        if profile_type == 0:
            # Strong
            c10, c12, m, p, c, ent = random.uniform(88, 96), random.uniform(88, 95), random.uniform(85, 98), random.uniform(82, 95), random.uniform(80, 94), random.uniform(85, 96)
        elif profile_type == 1:
            # Average
            c10, c12, m, p, c, ent = random.uniform(72, 85), random.uniform(74, 84), random.uniform(70, 82), random.uniform(65, 80), random.uniform(65, 78), random.uniform(70, 82)
        elif profile_type == 2:
            # Borderline
            c10, c12, m, p, c, ent = random.uniform(62, 70), random.uniform(60, 66), random.uniform(58, 64), random.uniform(52, 60), random.uniform(52, 60), random.uniform(60, 68)
        else:
            # Ineligible
            c10, c12, m, p, c, ent = random.uniform(50, 60), random.uniform(48, 56), random.uniform(45, 54), random.uniform(42, 52), random.uniform(40, 50), random.uniform(35, 52)
            
        academic_data = {
            'class10_percentage': round(c10, 1),
            'class12_percentage': round(c12, 1),
            'mathematics': round(m, 1),
            'physics': round(p, 1),
            'chemistry': round(c, 1),
            'entrance_exam': 'JEE Main' if i % 2 == 0 else 'CUET',
            'entrance_score': round(ent, 1),
            'passing_year': 2025,
            'school_board': 'CBSE' if i % 2 == 0 else 'ICSE',
            'achievements': f"Achievement {i}" if profile_type < 2 else "",
            'certifications': f"Certification {i}" if profile_type < 2 else "",
            'extracurricular': "Sports / Coding Club",
            'work_experience': "",
            'sop': f"Statement of purpose for {name} pursuing {course}."
        }
        Application.save_academic_info(a_id, academic_data)
        
        # Upload mandatory documents
        DocumentModel.add(a_id, "Class 10 Marksheet", f"uploads/{a_num}_c10.pdf", f"{a_num}_c10.pdf", f"Verified Class 10 record for {name}", "VERIFIED", "OCR Match 100%")
        DocumentModel.add(a_id, "Class 12 Marksheet", f"uploads/{a_num}_c12.pdf", f"{a_num}_c12.pdf", f"Verified Class 12 record for {name}", "VERIFIED", "OCR Match 100%")
        DocumentModel.add(a_id, "Entrance Scorecard", f"uploads/{a_num}_jee.pdf", f"{a_num}_jee.pdf", f"Verified Scorecard for {name}", "VERIFIED", "NTA Authenticated", is_digilocker=1)
        DocumentModel.add(a_id, "Identity Proof", f"uploads/{a_num}_id.pdf", f"{a_num}_id.pdf", f"Aadhaar Record for {name}", "VERIFIED", "DigiLocker Verified", is_digilocker=1)
        
        # Eligibility
        is_elig, summary = evaluate_eligibility(course, academic_data)
        execute_db("INSERT INTO eligibility_results (application_id, is_eligible, summary_json) VALUES (?, ?, ?)", (a_id, 1 if is_elig else 0, json.dumps(summary)))
        
        # AI Recommendation
        p_res = predict_admission_suitability(academic_data)
        x_res = generate_explainability(p_res['feature_dict'], p_res['suitability_score'], course)
        AIInfo.save(a_id, p_res['suitability_score'], p_res['recommendation'], x_res['feature_importance'], x_res)
        
        # Assign statuses & officer decisions for populated dashboard
        if i % 5 == 1:
            Application.update_status(a_id, 'OFFICER_REVIEW')
        elif i % 5 == 2:
            execute_db("INSERT INTO officer_decisions (application_id, officer_id, decision, comments, is_override) VALUES (?, ?, 'ACCEPTED', 'Excellent academic profile and entrance score.', 0)", (a_id, admin_id))
            Application.update_status(a_id, 'ACCEPTED')
        elif i % 5 == 3:
            execute_db("INSERT INTO officer_decisions (application_id, officer_id, decision, comments, is_override) VALUES (?, ?, 'REJECTED', 'Does not meet minimum entrance requirement for course.', 0)", (a_id, admin_id))
            Application.update_status(a_id, 'REJECTED')
        elif i % 5 == 4:
            execute_db("INSERT INTO officer_decisions (application_id, officer_id, decision, comments, is_override) VALUES (?, ?, 'ON_HOLD', 'Awaiting original transfer certificate verification.', 1)", (a_id, admin_id))
            Application.update_status(a_id, 'ON_HOLD')
        else:
            Application.update_status(a_id, 'OFFICER_REVIEW')
            
    print("=== Seeding Successfully Completed ===")
    print("Demo Admin Credentials:   admin@university.edu / admin123")
    print("Demo Student Credentials: soumya@example.com / student123")

if __name__ == '__main__':
    seed_database()
