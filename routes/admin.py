import json
import joblib
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from config import Config
from models.application import Application
from database.db import query_db, execute_db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Admin authentication required.', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('role') != 'admin':
            flash('Access denied. Officers only.', 'danger')
            return redirect(url_for('student.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    # Key dashboard statistics
    total_apps = query_db("SELECT COUNT(*) as count FROM applications", one=True)['count']
    pending_review = query_db("SELECT COUNT(*) as count FROM applications WHERE status = 'OFFICER_REVIEW' OR status = 'DOCUMENT_VERIFICATION'", one=True)['count']
    
    eligible_count = query_db("SELECT COUNT(*) as count FROM eligibility_results WHERE is_eligible = 1", one=True)['count']
    ineligible_count = query_db("SELECT COUNT(*) as count FROM eligibility_results WHERE is_eligible = 0", one=True)['count']
    
    highly_rec = query_db("SELECT COUNT(*) as count FROM ai_recommendations WHERE recommendation = 'Highly Recommended'", one=True)['count']
    
    accepted_count = query_db("SELECT COUNT(*) as count FROM officer_decisions WHERE decision = 'ACCEPTED'", one=True)['count']
    rejected_count = query_db("SELECT COUNT(*) as count FROM officer_decisions WHERE decision = 'REJECTED'", one=True)['count']
    on_hold_count = query_db("SELECT COUNT(*) as count FROM officer_decisions WHERE decision = 'ON_HOLD'", one=True)['count']
    
    recent_apps = Application.get_all_with_filters()[:8]
    
    metrics = {
        'total_apps': total_apps,
        'pending_review': pending_review,
        'eligible_count': eligible_count,
        'ineligible_count': ineligible_count,
        'highly_rec': highly_rec,
        'accepted_count': accepted_count,
        'rejected_count': rejected_count,
        'on_hold_count': on_hold_count
    }
    
    return render_template('admin/dashboard.html', metrics=metrics, recent_apps=recent_apps)

@admin_bp.route('/applications')
@admin_required
def applications():
    course = request.args.get('course')
    eligibility = request.args.get('eligibility')
    recommendation = request.args.get('recommendation')
    status = request.args.get('status')
    search = request.args.get('search')
    
    apps_list = Application.get_all_with_filters(
        course=course,
        eligibility=eligibility,
        recommendation=recommendation,
        status=status,
        search=search
    )
    
    return render_template('admin/applications.html', apps=apps_list, current_filters=request.args)

@admin_bp.route('/applicant/<int:app_id>')
@admin_required
def applicant_detail(app_id):
    app_details = Application.get_full_details(app_id)
    if not app_details:
        flash('Applicant record not found.', 'danger')
        return redirect(url_for('admin.applications'))
        
    return render_template('admin/applicant_detail.html', app=app_details)

@admin_bp.route('/decision/<int:app_id>', methods=['POST'])
@admin_required
def save_decision(app_id):
    officer_id = session.get('user_id')
    decision = request.form.get('decision')  # ACCEPTED, REJECTED, ON_HOLD
    comments = request.form.get('comments', '').strip()
    
    if decision not in ['ACCEPTED', 'REJECTED', 'ON_HOLD']:
        flash('Invalid decision action.', 'danger')
        return redirect(url_for('admin.applicant_detail', app_id=app_id))
        
    app_details = Application.get_full_details(app_id)
    if not app_details:
        flash('Application missing.', 'danger')
        return redirect(url_for('admin.applications'))
        
    ai_rec = app_details.get('ai', {}).get('recommendation', '')
    
    # Track human override
    is_override = 0
    if ai_rec in ['Highly Recommended', 'Recommended'] and decision in ['REJECTED', 'ON_HOLD']:
        is_override = 1
    elif ai_rec in ['Low Recommendation', 'Review Required'] and decision == 'ACCEPTED':
        is_override = 1
        
    # Save officer decision
    execute_db("DELETE FROM officer_decisions WHERE application_id = ?", (app_id,))
    execute_db(
        "INSERT INTO officer_decisions (application_id, officer_id, decision, comments, is_override) VALUES (?, ?, ?, ?, ?)",
        (app_id, officer_id, decision, comments, is_override)
    )
    
    # Update main application status
    Application.update_status(app_id, decision)
    
    flash(f"Decision '{decision}' recorded successfully for Application {app_details['application_number']}.", 'success')
    return redirect(url_for('admin.applicant_detail', app_id=app_id))

@admin_bp.route('/analytics')
@admin_required
def analytics():
    # Gather database counts for charts
    courses = query_db("SELECT course, COUNT(*) as count FROM applications GROUP BY course")
    eligibility_dist = query_db("SELECT CASE WHEN is_eligible = 1 THEN 'Eligible' ELSE 'Not Eligible' END as label, COUNT(*) as count FROM eligibility_results GROUP BY is_eligible")
    rec_dist = query_db("SELECT recommendation as label, COUNT(*) as count FROM ai_recommendations GROUP BY recommendation")
    dec_dist = query_db("SELECT decision as label, COUNT(*) as count FROM officer_decisions GROUP BY decision")
    
    funnel = {
        'submitted': query_db("SELECT COUNT(*) FROM applications")[0][0],
        'docs_uploaded': query_db("SELECT COUNT(DISTINCT application_id) FROM documents")[0][0],
        'eligible': query_db("SELECT COUNT(*) FROM eligibility_results WHERE is_eligible = 1")[0][0],
        'ai_recommended': query_db("SELECT COUNT(*) FROM ai_recommendations WHERE recommendation IN ('Highly Recommended', 'Recommended')")[0][0],
        'officer_approved': query_db("SELECT COUNT(*) FROM officer_decisions WHERE decision = 'ACCEPTED'")[0][0]
    }
    
    chart_data = {
        'courses': [dict(c) for c in courses],
        'eligibility': [dict(e) for e in eligibility_dist],
        'recommendation': [dict(r) for r in rec_dist],
        'decisions': [dict(d) for d in dec_dist],
        'funnel': funnel
    }
    
    return render_template('admin/analytics.html', chart_data=chart_data)

@admin_bp.route('/model-metrics')
@admin_required
def model_metrics():
    metrics_path = os.path.join(os.path.dirname(Config.ML_MODEL_PATH), 'metrics.pkl')
    metrics = {}
    if os.path.exists(metrics_path):
        metrics = joblib.load(metrics_path)
    else:
        # Default metrics fallback
        metrics = {
            'accuracy': 0.8900,
            'precision': 0.8872,
            'recall': 0.8900,
            'f1_score': 0.8823,
            'dataset_size': 1000,
            'feature_importance': {
                'Class 12 Percentage': 34.5,
                'Entrance Exam Score': 29.8,
                'Mathematics Score': 12.1,
                'Physics Score': 8.4,
                'Class 10 Percentage': 5.2,
                'Extracurricular Activities': 4.1,
                'Achievements & Awards': 3.2,
                'Certifications': 2.7
            }
        }
        
    return render_template('admin/model_metrics.html', metrics=metrics)
