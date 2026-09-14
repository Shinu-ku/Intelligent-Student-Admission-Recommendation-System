import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'university-admission-ai-secret-key-2026-prod'
    DATABASE = os.path.join(BASE_DIR, 'database', 'admission_system.db')
    SCHEMA = os.path.join(BASE_DIR, 'database', 'schema.sql')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max limit
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
    
    # ML Model Config
    ML_MODEL_PATH = os.path.join(BASE_DIR, 'ml', 'model.pkl')
    ML_SCALER_PATH = os.path.join(BASE_DIR, 'ml', 'scaler.pkl')
    ML_DATASET_PATH = os.path.join(BASE_DIR, 'ml', 'dataset.csv')
