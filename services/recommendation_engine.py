import os
import joblib
import numpy as np
from config import Config

_model = None
_scaler = None

def load_ml_model():
    global _model, _scaler
    if _model is None or _scaler is None:
        if os.path.exists(Config.ML_MODEL_PATH) and os.path.exists(Config.ML_SCALER_PATH):
            _model = joblib.load(Config.ML_MODEL_PATH)
            _scaler = joblib.load(Config.ML_SCALER_PATH)
        else:
            # Train on demand if model file missing
            from ml.train_model import train_and_save_model
            _model, _scaler, _ = train_and_save_model()
    return _model, _scaler

def predict_admission_suitability(academic_info):
    """
    Computes suitability score (0-100%) and recommendation category for an application.
    """
    model, scaler = load_ml_model()
    
    # Extract features
    c10 = float(academic_info.get('class10_percentage', 75.0))
    c12 = float(academic_info.get('class12_percentage', 75.0))
    math = float(academic_info.get('mathematics', 75.0))
    phys = float(academic_info.get('physics', 75.0))
    chem = float(academic_info.get('chemistry', 75.0))
    entrance = float(academic_info.get('entrance_score', 75.0))
    
    academic_consistency = max(50.0, min(100.0, 100.0 - abs(c12 - c10)))
    
    # Count achievements and certifications
    achievements = academic_info.get('achievements', '') or ''
    achievements_count = len([a for a in achievements.split('\n') if a.strip()]) if isinstance(achievements, str) else int(achievements)
    achievements_count = min(5, achievements_count)
    
    certs = academic_info.get('certifications', '') or ''
    certs_count = len([c for c in certs.split('\n') if c.strip()]) if isinstance(certs, str) else int(certs)
    certs_count = min(5, certs_count)
    
    extracurricular = academic_info.get('extracurricular', '') or ''
    extra_score = 75.0 if extracurricular else 50.0
    
    features = np.array([[
        c10, c12, math, phys, chem, entrance, academic_consistency,
        achievements_count, certs_count, extra_score
    ]])
    
    scaled_features = scaler.transform(features)
    probs = model.predict_proba(scaled_features)[0]
    
    # Calculate weighted continuous score (0-100%)
    weighted_score = (
        0.35 * c12 +
        0.30 * entrance +
        0.12 * math +
        0.08 * phys +
        0.05 * chem +
        0.04 * extra_score +
        0.03 * (achievements_count + certs_count) * 5 +
        0.03 * academic_consistency
    )
    suitability_score = round(float(np.clip(weighted_score, 35.0, 98.0)), 1)
    
    if suitability_score >= 85.0:
        recommendation = 'Highly Recommended'
    elif suitability_score >= 70.0:
        recommendation = 'Recommended'
    elif suitability_score >= 55.0:
        recommendation = 'Review Required'
    else:
        recommendation = 'Low Recommendation'
        
    feature_dict = {
        'class10_percentage': c10,
        'class12_percentage': c12,
        'mathematics': math,
        'physics': phys,
        'chemistry': chem,
        'entrance_score': entrance,
        'academic_consistency': academic_consistency,
        'achievements_count': achievements_count,
        'certifications_count': certs_count,
        'extracurricular_score': extra_score
    }
    
    return {
        'suitability_score': suitability_score,
        'recommendation': recommendation,
        'feature_dict': feature_dict
    }
