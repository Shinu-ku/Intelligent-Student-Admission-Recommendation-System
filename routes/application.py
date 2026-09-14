from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.application import Application
from models.user import User
from routes.student import student_required

app_bp = Blueprint('application', __name__, url_prefix='/application')

COURSES = [
    'B.Tech Computer Science & Engineering',
    'B.Tech Information Technology',
    'B.Tech Electronics & Communication',
    'B.Tech Mechanical Engineering',
    'B.Tech Electrical Engineering'
]

@app_bp.route('/apply', methods=['GET', 'POST'])
@student_required
def apply():
    user_id = session.get('user_id')
    user = User.find_by_id(user_id)
    
    # Check if student already has an active application
    existing_apps = Application.find_by_student(user_id)
    existing_app_data = None
    if existing_apps:
        existing_app_data = Application.get_full_details(existing_apps[0]['id'])
        
    if request.method == 'POST':
        course = request.form.get('course', 'B.Tech Computer Science & Engineering')
        
        # Collect academic info
        c10 = request.form.get('class10_percentage')
        c12 = request.form.get('class12_percentage')
        math = request.form.get('mathematics')
        phys = request.form.get('physics')
        chem = request.form.get('chemistry')
        entrance_exam = request.form.get('entrance_exam', 'JEE Main')
        entrance_score = request.form.get('entrance_score')
        passing_year = request.form.get('passing_year', '2025')
        school_board = request.form.get('school_board', 'CBSE')
        
        achievements = request.form.get('achievements', '')
        certifications = request.form.get('certifications', '')
        extracurricular = request.form.get('extracurricular', '')
        work_experience = request.form.get('work_experience', '')
        sop = request.form.get('sop', '')
        
        # Validation
        try:
            c10_val = float(c10)
            c12_val = float(c12)
            math_val = float(math)
            phys_val = float(phys)
            chem_val = float(chem)
            entrance_val = float(entrance_score)
        except (ValueError, TypeError):
            flash('Please enter valid numeric percentage and mark values.', 'danger')
            return render_template('student/apply.html', user=user, courses=COURSES, app_data=existing_app_data)
            
        if existing_apps:
            app_id = existing_apps[0]['id']
            app_num = existing_apps[0]['application_number']
        else:
            app_id, app_num = Application.create(user_id, course)
            
        # Save academic data
        academic_payload = {
            'class10_percentage': c10_val,
            'class12_percentage': c12_val,
            'mathematics': math_val,
            'physics': phys_val,
            'chemistry': chem_val,
            'entrance_exam': entrance_exam,
            'entrance_score': entrance_val,
            'passing_year': passing_year,
            'school_board': school_board,
            'achievements': achievements,
            'certifications': certifications,
            'extracurricular': extracurricular,
            'work_experience': work_experience,
            'sop': sop
        }
        
        Application.save_academic_info(app_id, academic_payload)
        Application.update_status(app_id, 'DOCUMENTS_PENDING')
        
        flash(f'Application {app_num} submitted successfully! Please upload your required documents.', 'success')
        return redirect(url_for('documents.manage_documents'))
        
    return render_template('student/apply.html', user=user, courses=COURSES, app_data=existing_app_data)
