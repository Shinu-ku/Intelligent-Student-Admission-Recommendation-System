import os
import sys
from flask import Flask, render_template, session, redirect, url_for

from config import Config
from database.db import close_db, init_db
from routes.auth import auth_bp
from routes.student import student_bp
from routes.application import app_bp
from routes.documents import docs_bp
from routes.eligibility import eligibility_bp
from routes.ai import ai_bp
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Teardown DB connection
    app.teardown_appcontext(close_db)

    # Initialize Database Schema if DB missing
    if not os.path.exists(Config.DATABASE):
        with app.app_context():
            init_db(app)

    # Check or Train ML Model
    if not os.path.exists(Config.ML_MODEL_PATH):
        try:
            from ml.train_model import train_and_save_model
            train_and_save_model()
        except Exception as e:
            print(f"Warning: Unable to initialize ML model on startup: {e}")

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(app_bp)
    app.register_blueprint(docs_bp)
    app.register_blueprint(eligibility_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(admin_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', content="<div class='container py-5 text-center'><h1 class='text-danger display-1'>404</h1><h3 class='text-white'>Page Not Found</h3><p class='text-secondary'>The requested page URI does not exist.</p><a href='/' class='btn btn-primary-custom mt-3'>Return to Home</a></div>"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('base.html', content="<div class='container py-5 text-center'><h1 class='text-warning display-1'>500</h1><h3 class='text-white'>Internal Application Error</h3><p class='text-secondary'>An error occurred while processing your request. Please try again.</p><a href='/' class='btn btn-primary-custom mt-3'>Return to Home</a></div>"), 500

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return render_template('base.html', content="<div class='container py-5 text-center'><h1 class='text-danger display-1'>413</h1><h3 class='text-white'>File Too Large</h3><p class='text-secondary'>Uploaded document exceeds maximum size limit of 16MB.</p><a href='/documents/manage' class='btn btn-primary-custom mt-3'>Back to Documents</a></div>"), 413

    return app

app = create_app()

if __name__ == '__main__':
    print("=== Starting Intelligent Student Admission Recommendation System ===")
    print("Access URL: http://127.0.0.1:5000")
    print("Demo Admin Credentials:   admin@university.edu / admin123")
    print("Demo Student Credentials: soumya@example.com / student123")
    app.run(debug=True, host='127.0.0.1', port=5000)
