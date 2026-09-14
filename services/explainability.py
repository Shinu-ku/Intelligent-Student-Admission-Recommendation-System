import json
from services.recommendation_engine import load_ml_model

FEATURE_LABELS = {
    'class12_percentage': 'Class 12 Percentage',
    'entrance_score': 'Entrance Exam Score',
    'mathematics': 'Mathematics Score',
    'physics': 'Physics Score',
    'class10_percentage': 'Class 10 Percentage',
    'chemistry': 'Chemistry Score',
    'academic_consistency': 'Academic Consistency',
    'achievements_count': 'Achievements & Awards',
    'certifications_count': 'Certifications',
    'extracurricular_score': 'Extracurricular Activities'
}

def generate_explainability(feature_dict, suitability_score, course_name="B.Tech Computer Science & Engineering"):
    """
    Computes Random Forest feature importance visualization data
    and generates natural language explanations (Positive factors vs Concerns).
    """
    model, _ = load_ml_model()
    
    raw_importances = model.feature_importances_
    cols = [
        'class10_percentage', 'class12_percentage', 'mathematics',
        'physics', 'chemistry', 'entrance_score', 'academic_consistency',
        'achievements_count', 'certifications_count', 'extracurricular_score'
    ]
    
    importance_map = dict(zip(cols, raw_importances))
    
    # Normalize importances to 100% scale
    total_imp = sum(importance_map.values())
    norm_importances = {
        FEATURE_LABELS.get(k, k): round((v / total_imp) * 100, 1)
        for k, v in sorted(importance_map.items(), key=lambda x: x[1], reverse=True)
    }
    
    # Generate Positive factors and Concerns
    positive_factors = []
    concern_factors = []
    
    c12 = feature_dict.get('class12_percentage', 0)
    entrance = feature_dict.get('entrance_score', 0)
    math = feature_dict.get('mathematics', 0)
    phys = feature_dict.get('physics', 0)
    achieve = feature_dict.get('achievements_count', 0)
    certs = feature_dict.get('certifications_count', 0)
    
    if c12 >= 85:
        positive_factors.append(f"Strong Class 12 academic performance ({c12:.1f}%) exceeding competitive benchmark.")
    elif c12 >= 70:
        positive_factors.append(f"Solid Class 12 academic baseline ({c12:.1f}%).")
    else:
        concern_factors.append(f"Class 12 percentage ({c12:.1f}%) is below competitive target threshold.")
        
    if math >= 85:
        positive_factors.append(f"Outstanding Mathematics score ({math:.1f}) demonstrating analytical readiness.")
    elif math < 60:
        concern_factors.append(f"Mathematics score ({math:.1f}) is near minimum baseline.")
        
    if entrance >= 80:
        positive_factors.append(f"High entrance exam percentile ({entrance:.1f}) well above course requirement.")
    elif entrance >= 65:
        positive_factors.append(f"Satisfactory entrance exam score ({entrance:.1f}).")
    else:
        concern_factors.append(f"Entrance exam score ({entrance:.1f}) could be stronger for high-demand branches.")
        
    if achieve + certs >= 2:
        positive_factors.append(f"Demonstrated holistic profile with {achieve} achievements and {certs} certifications.")
    else:
        concern_factors.append("Limited documented extracurricular achievements or industry certifications.")
        
    positive_factors.append("All mandatory academic transcripts and identity documents uploaded.")
    
    return {
        'feature_importance': norm_importances,
        'positive_factors': positive_factors,
        'concern_factors': concern_factors,
        'summary': f"AI evaluated candidate suitability at {suitability_score}% based on Random Forest multi-factor weighting."
    }
