import json
from database.db import query_db, execute_db

class AIInfo:
    @staticmethod
    def save(application_id, suitability_score, recommendation, feature_importance, explanation, model_version="v1.0-RandomForest"):
        execute_db("DELETE FROM ai_recommendations WHERE application_id = ?", (application_id,))
        
        sql = """
            INSERT INTO ai_recommendations (
                application_id, suitability_score, recommendation,
                feature_importance_json, explanation_json, model_version
            ) VALUES (?, ?, ?, ?, ?, ?)
        """
        f_json = json.dumps(feature_importance)
        e_json = json.dumps(explanation)
        return execute_db(sql, (
            application_id, suitability_score, recommendation, f_json, e_json, model_version
        ))

    @staticmethod
    def get_by_application(application_id):
        sql = "SELECT * FROM ai_recommendations WHERE application_id = ?"
        res = query_db(sql, (application_id,), one=True)
        if not res:
            return None
        res_dict = dict(res)
        res_dict['feature_importance'] = json.loads(res_dict['feature_importance_json'])
        res_dict['explanation'] = json.loads(res_dict['explanation_json'])
        return res_dict
