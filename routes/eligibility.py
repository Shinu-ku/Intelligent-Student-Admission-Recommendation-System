import json
from flask import Blueprint, render_template, redirect, url_for, flash, session
from models.application import Application
from database.db import execute_db, query_db
from services.eligibility_engine import evaluate_eligibility
from routes.student import student_required

eligibility_bp = Blueprint('eligibility', __name__, url_prefix='/eligibility')

@eligibility_bp.route('/check')
@student_required
def check_eligibility():
    user_id = session.get('user_id')
    apps = Application.find_by_student(user_id)
    
    if not apps:
        flash('Please complete your application first.', 'warning')
        return redirect(url_for('application.apply'))
        
    app_details = Application.get_full_details(apps[0]['id'])
    academic = app_details.get('academic')
    
    if not academic:
        flash('Academic details missing. Please complete the application form.', 'danger')
        return redirect(url_for('application.apply'))
        
    course = app_details['course']
    is_eligible, summary = evaluate_eligibility(course, academic)
    
    # Save or update eligibility result in database
    execute_db("DELETE FROM eligibility_results WHERE application_id = ?", (app_details['id'],))
    execute_db(
        "INSERT INTO eligibility_results (application_id, is_eligible, summary_json) VALUES (?, ?, ?)",
        (app_details['id'], 1 if is_eligible else 0, json.dumps(summary))
    )
    
    Application.update_status(app_details['id'], 'ELIGIBILITY_REVIEW')
    
    return render_template('student/eligibility.html', app=app_details, eligibility=summary)
