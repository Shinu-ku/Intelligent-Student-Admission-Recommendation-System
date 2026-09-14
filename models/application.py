import json
import random
from database.db import query_db, execute_db

class Application:
    @staticmethod
    def generate_app_number():
        seq = random.randint(1000, 9999)
        return f"APP-2026-{seq}"

    @staticmethod
    def create(student_id, course):
        app_num = Application.generate_app_number()
        sql = """
            INSERT INTO applications (student_id, application_number, course, status)
            VALUES (?, ?, ?, 'DRAFT')
        """
        app_id = execute_db(sql, (student_id, app_num, course))
        return app_id, app_num

    @staticmethod
    def find_by_student(student_id):
        sql = "SELECT * FROM applications WHERE student_id = ? ORDER BY id DESC"
        return query_db(sql, (student_id,))

    @staticmethod
    def find_by_id(app_id):
        sql = "SELECT * FROM applications WHERE id = ?"
        return query_db(sql, (app_id,), one=True)

    @staticmethod
    def get_full_details(app_id):
        app = query_db("SELECT a.*, u.full_name, u.email, u.phone, u.dob FROM applications a JOIN users u ON a.student_id = u.id WHERE a.id = ?", (app_id,), one=True)
        if not app:
            return None
        
        app_dict = dict(app)
        
        # Academic info
        academic = query_db("SELECT * FROM academic_info WHERE application_id = ?", (app_id,), one=True)
        app_dict['academic'] = dict(academic) if academic else None
        
        # Documents
        docs = query_db("SELECT * FROM documents WHERE application_id = ?", (app_id,))
        app_dict['documents'] = [dict(d) for d in docs] if docs else []
        
        # Eligibility
        elig = query_db("SELECT * FROM eligibility_results WHERE application_id = ?", (app_id,), one=True)
        if elig:
            elig_dict = dict(elig)
            elig_dict['summary'] = json.loads(elig_dict['summary_json'])
            app_dict['eligibility'] = elig_dict
        else:
            app_dict['eligibility'] = None
            
        # AI Recommendation
        ai = query_db("SELECT * FROM ai_recommendations WHERE application_id = ?", (app_id,), one=True)
        if ai:
            ai_dict = dict(ai)
            ai_dict['feature_importance'] = json.loads(ai_dict['feature_importance_json'])
            ai_dict['explanation'] = json.loads(ai_dict['explanation_json'])
            app_dict['ai'] = ai_dict
        else:
            app_dict['ai'] = None
            
        # Officer Decision
        decision = query_db("SELECT d.*, u.full_name as officer_name FROM officer_decisions d JOIN users u ON d.officer_id = u.id WHERE d.application_id = ?", (app_id,), one=True)
        app_dict['decision'] = dict(decision) if decision else None
        
        return app_dict

    @staticmethod
    def save_academic_info(app_id, academic_data):
        sql = """
            INSERT OR REPLACE INTO academic_info (
                application_id, class10_percentage, class12_percentage,
                mathematics, physics, chemistry, entrance_exam, entrance_score,
                passing_year, school_board, achievements, certifications,
                extracurricular, work_experience, sop
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        execute_db(sql, (
            app_id,
            float(academic_data['class10_percentage']),
            float(academic_data['class12_percentage']),
            float(academic_data['mathematics']),
            float(academic_data['physics']),
            float(academic_data['chemistry']),
            academic_data['entrance_exam'],
            float(academic_data['entrance_score']),
            int(academic_data['passing_year']),
            academic_data['school_board'],
            academic_data.get('achievements', ''),
            academic_data.get('certifications', ''),
            academic_data.get('extracurricular', ''),
            academic_data.get('work_experience', ''),
            academic_data.get('sop', '')
        ))

    @staticmethod
    def update_status(app_id, status):
        sql = "UPDATE applications SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        execute_db(sql, (status, app_id))

    @staticmethod
    def get_all_with_filters(course=None, eligibility=None, recommendation=None, status=None, search=None):
        sql = """
            SELECT a.id, a.application_number, a.course, a.status, a.submitted_at,
                   u.full_name as student_name, u.email,
                   ac.class12_percentage, ac.entrance_score,
                   e.is_eligible,
                   ai.suitability_score, ai.recommendation,
                   d.decision as officer_decision
            FROM applications a
            JOIN users u ON a.student_id = u.id
            LEFT JOIN academic_info ac ON a.id = ac.application_id
            LEFT JOIN eligibility_results e ON a.id = e.application_id
            LEFT JOIN ai_recommendations ai ON a.id = ai.application_id
            LEFT JOIN officer_decisions d ON a.id = d.application_id
            WHERE 1=1
        """
        params = []
        if course:
            sql += " AND a.course = ?"
            params.append(course)
        if eligibility:
            if eligibility == 'Eligible':
                sql += " AND e.is_eligible = 1"
            elif eligibility == 'Not Eligible':
                sql += " AND e.is_eligible = 0"
        if recommendation:
            sql += " AND ai.recommendation = ?"
            params.append(recommendation)
        if status:
            sql += " AND a.status = ?"
            params.append(status)
        if search:
            sql += " AND (u.full_name LIKE ? OR a.application_number LIKE ? OR u.email LIKE ?)"
            term = f"%{search}%"
            params.extend([term, term, term])
            
        sql += " ORDER BY a.id DESC"
        return query_db(sql, params)
