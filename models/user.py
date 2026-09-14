from werkzeug.security import generate_password_hash, check_password_hash
from database.db import query_db, execute_db

class User:
    @staticmethod
    def create(full_name, email, password, role='student', phone=None, dob=None):
        password_hash = generate_password_hash(password)
        sql = """
            INSERT INTO users (full_name, email, password_hash, role, phone, dob)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        user_id = execute_db(sql, (full_name, email, password_hash, role, phone, dob))
        return user_id

    @staticmethod
    def find_by_email(email):
        sql = "SELECT * FROM users WHERE email = ?"
        return query_db(sql, (email,), one=True)

    @staticmethod
    def find_by_id(user_id):
        sql = "SELECT * FROM users WHERE id = ?"
        return query_db(sql, (user_id,), one=True)

    @staticmethod
    def verify_password(stored_hash, password):
        return check_password_hash(stored_hash, password)
