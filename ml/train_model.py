import os
import sys
import joblib
import pandas as pd
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

from config import Config
from ml.dataset_generator import generate_synthetic_dataset

FEATURE_COLUMNS = [
    'class10_percentage',
    'class12_percentage',
    'mathematics',
    'physics',
    'chemistry',
    'entrance_score',
    'academic_consistency',
    'achievements_count',
    'certifications_count',
    'extracurricular_score'
]

def train_and_save_model():
    if not os.path.exists(Config.ML_DATASET_PATH):
        df = generate_synthetic_dataset(1000, Config.ML_DATASET_PATH)
    else:
        df = pd.read_csv(Config.ML_DATASET_PATH)
        
    X = df[FEATURE_COLUMNS]
    y = df['category_code']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight='balanced'
    )
    rf.fit(X_train_scaled, y_train)
    
    y_pred = rf.predict(X_test_scaled)
    
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'precision': float(precision_score(y_test, y_pred, average='weighted')),
        'recall': float(recall_score(y_test, y_pred, average='weighted')),
        'f1_score': float(f1_score(y_test, y_pred, average='weighted')),
        'dataset_size': len(df),
        'feature_importance': dict(zip(FEATURE_COLUMNS, [float(v) for v in rf.feature_importances_]))
    }
    
    os.makedirs(os.path.dirname(Config.ML_MODEL_PATH), exist_ok=True)
    joblib.dump(rf, Config.ML_MODEL_PATH)
    joblib.dump(scaler, Config.ML_SCALER_PATH)
    joblib.dump(metrics, os.path.join(os.path.dirname(Config.ML_MODEL_PATH), 'metrics.pkl'))
    
    print("=== Random Forest Model Training Complete ===")
    print(f"Accuracy:  {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1 Score:  {metrics['f1_score']:.4f}")
    print("Model saved to:", Config.ML_MODEL_PATH)
    
    return rf, scaler, metrics

if __name__ == '__main__':
    train_and_save_model()
