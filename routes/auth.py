from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('student.dashboard' if session.get('role') == 'student' else 'admin.dashboard'))
        
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        phone = request.form.get('phone', '').strip()
        dob = request.form.get('dob', '').strip()
        
        # Validations
        if not full_name or not email or not password:
            flash('All required fields must be filled.', 'danger')
            return render_template('register.html')
            
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return render_template('register.html')
            
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
            
        existing_user = User.find_by_email(email)
        if existing_user:
            flash('An account with this email already exists.', 'warning')
            return render_template('register.html')
            
        try:
            user_id = User.create(full_name, email, password, role='student', phone=phone, dob=dob)
            session['user_id'] = user_id
            session['full_name'] = full_name
            session['email'] = email
            session['role'] = 'student'
            flash('Registration successful! Welcome to your admission portal.', 'success')
            return redirect(url_for('student.dashboard'))
        except Exception as e:
            flash(f'Error creating account: {str(e)}', 'danger')
            
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('student.dashboard' if session.get('role') == 'student' else 'admin.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        user = User.find_by_email(email)
        if user and User.verify_password(user['password_hash'], password):
            session['user_id'] = user['id']
            session['full_name'] = user['full_name']
            session['email'] = user['email']
            session['role'] = user['role']
            flash(f"Welcome back, {user['full_name']}!", 'success')
            
            if user['role'] == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('student.dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))
