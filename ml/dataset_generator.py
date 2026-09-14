import os
import sys
import numpy as np
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

def generate_synthetic_dataset(num_samples=1000, save_path=None):
    np.random.seed(42)
    
    # Generate realistic correlated features
    class10 = np.random.normal(78, 10, num_samples).clip(50, 99)
    # Class 12 correlated with Class 10
    class12 = (0.7 * class10 + np.random.normal(23, 8, num_samples)).clip(50, 99)
    
    # Subject scores correlated with Class 12
    mathematics = (0.75 * class12 + np.random.normal(20, 10, num_samples)).clip(40, 100)
    physics = (0.70 * class12 + np.random.normal(25, 10, num_samples)).clip(40, 100)
    chemistry = (0.68 * class12 + np.random.normal(27, 10, num_samples)).clip(40, 100)
    
    # Entrance exam score (correlated with class 12 and maths)
    entrance_score = (0.4 * class12 + 0.4 * mathematics + np.random.normal(15, 12, num_samples)).clip(30, 100)
    
    academic_consistency = (100 - np.abs(class12 - class10)).clip(50, 100)
    achievements_count = np.random.poisson(1.2, num_samples).clip(0, 5)
    certifications_count = np.random.poisson(1.0, num_samples).clip(0, 5)
    extracurricular_score = np.random.normal(70, 15, num_samples).clip(30, 100)
    
    # Calculate synthetic suitability target (0-100)
    composite_score = (
        0.35 * class12 +
        0.30 * entrance_score +
        0.12 * mathematics +
        0.08 * physics +
        0.05 * chemistry +
        0.04 * extracurricular_score +
        0.03 * (achievements_count + certifications_count) * 5 +
        0.03 * academic_consistency
    ) + np.random.normal(0, 2.5, num_samples)
    
    composite_score = composite_score.clip(35, 98)
    
    # Map to recommendation category labels
    recommendation_labels = []
    category_codes = []
    for score in composite_score:
        if score >= 85:
            recommendation_labels.append('Highly Recommended')
            category_codes.append(3)
        elif score >= 70:
            recommendation_labels.append('Recommended')
            category_codes.append(2)
        elif score >= 55:
            recommendation_labels.append('Review Required')
            category_codes.append(1)
        else:
            recommendation_labels.append('Low Recommendation')
            category_codes.append(0)
            
    df = pd.DataFrame({
        'class10_percentage': np.round(class10, 2),
        'class12_percentage': np.round(class12, 2),
        'mathematics': np.round(mathematics, 2),
        'physics': np.round(physics, 2),
        'chemistry': np.round(chemistry, 2),
        'entrance_score': np.round(entrance_score, 2),
        'academic_consistency': np.round(academic_consistency, 2),
        'achievements_count': achievements_count,
        'certifications_count': certifications_count,
        'extracurricular_score': np.round(extracurricular_score, 2),
        'suitability_score': np.round(composite_score, 2),
        'recommendation_label': recommendation_labels,
        'category_code': category_codes
    })
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_csv(save_path, index=False)
        print(f"Synthetic dataset saved to {save_path} ({len(df)} records).")
        
    return df

if __name__ == '__main__':
    generate_synthetic_dataset(1000, Config.ML_DATASET_PATH)
