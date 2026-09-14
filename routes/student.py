from flask import Blueprint, render_template, redirect, url_for, flash, session
from models.application import Application
from models.user import User

student_bp = Blueprint('student', __name__, url_prefix='/student')

def student_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('role') != 'student':
            flash('Access restricted to students.', 'danger')
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/dashboard')
@student_required
def dashboard():
    user_id = session.get('user_id')
    user = User.find_by_id(user_id)
    apps = Application.find_by_student(user_id)
    
    current_app = None
    app_details = None
    
    if apps:
        latest_app_id = apps[0]['id']
        app_details = Application.get_full_details(latest_app_id)
        current_app = app_details
        
    return render_template('student/dashboard.html', user=user, app=current_app)
