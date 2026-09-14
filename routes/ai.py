from flask import Blueprint, render_template, redirect, url_for, flash, session
from models.application import Application
from models.ai_info import AIInfo
from services.recommendation_engine import predict_admission_suitability
from services.explainability import generate_explainability
from routes.student import student_required

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

@ai_bp.route('/analyze')
@student_required
def analyze():
    user_id = session.get('user_id')
    apps = Application.find_by_student(user_id)
    
    if not apps:
        flash('Please complete your application form first.', 'warning')
        return redirect(url_for('application.apply'))
        
    app_details = Application.get_full_details(apps[0]['id'])
    academic = app_details.get('academic')
    
    if not academic:
        flash('Academic information incomplete.', 'danger')
        return redirect(url_for('application.apply'))
        
    # Calculate suitability score via Random Forest
    pred = predict_admission_suitability(academic)
    suitability_score = pred['suitability_score']
    recommendation = pred['recommendation']
    
    # Calculate Explainability metrics
    xai = generate_explainability(pred['feature_dict'], suitability_score, app_details['course'])
    
    # Save to SQLite database
    AIInfo.save(
        app_details['id'],
        suitability_score,
        recommendation,
        xai['feature_importance'],
        {
            'positive_factors': xai['positive_factors'],
            'concern_factors': xai['concern_factors'],
            'summary': xai['summary']
        }
    )
    
    # Update application status to OFFICER_REVIEW
    Application.update_status(app_details['id'], 'OFFICER_REVIEW')
    
    # Refresh full details
    updated_app = Application.get_full_details(app_details['id'])
    
    return render_template(
        'student/ai_recommendation.html',
        app=updated_app,
        ai=updated_app.get('ai'),
        xai=xai
    )
