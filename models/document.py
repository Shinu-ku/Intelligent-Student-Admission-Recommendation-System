from database.db import query_db, execute_db

class DocumentModel:
    @staticmethod
    def add(application_id, document_type, file_path, file_name, ocr_text="", verification_status="PENDING", verification_message="", is_digilocker=0):
        # Remove old document of same type if present
        execute_db("DELETE FROM documents WHERE application_id = ? AND document_type = ?", (application_id, document_type))
        
        sql = """
            INSERT INTO documents (
                application_id, document_type, file_path, file_name,
                ocr_text, verification_status, verification_message, is_digilocker
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        doc_id = execute_db(sql, (
            application_id, document_type, file_path, file_name,
            ocr_text, verification_status, verification_message, is_digilocker
        ))
        return doc_id

    @staticmethod
    def get_by_application(application_id):
        sql = "SELECT * FROM documents WHERE application_id = ?"
        return query_db(sql, (application_id,))

    @staticmethod
    def delete(doc_id):
        execute_db("DELETE FROM documents WHERE id = ?", (doc_id,))
        
    @staticmethod
    def update_verification(doc_id, status, message, ocr_text=None, is_digilocker=None):
        sql = "UPDATE documents SET verification_status = ?, verification_message = ?"
        params = [status, message]
        if ocr_text is not None:
            sql += ", ocr_text = ?"
            params.append(ocr_text)
        if is_digilocker is not None:
            sql += ", is_digilocker = ?"
            params.append(is_digilocker)
        sql += " WHERE id = ?"
        params.append(doc_id)
        execute_db(sql, params)
