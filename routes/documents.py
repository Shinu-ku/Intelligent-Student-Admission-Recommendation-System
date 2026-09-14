import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from werkzeug.utils import secure_filename
from models.application import Application
from models.document import DocumentModel
from services.ocr_service import process_document_ocr
from routes.student import student_required

docs_bp = Blueprint('documents', __name__, url_prefix='/documents')

REQUIRED_DOCUMENTS = [
    'Class 10 Marksheet',
    'Class 12 Marksheet',
    'Entrance Scorecard',
    'Identity Proof',
    'Passport Photograph'
]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@docs_bp.route('/manage')
@student_required
def manage_documents():
    user_id = session.get('user_id')
    apps = Application.find_by_student(user_id)
    
    if not apps:
        flash('Please complete your application form before managing documents.', 'info')
        return redirect(url_for('application.apply'))
        
    app_details = Application.get_full_details(apps[0]['id'])
    
    # Determine document status list
    uploaded_docs = {d['document_type']: d for d in app_details['documents']}
    doc_checklist = []
    for doc_type in REQUIRED_DOCUMENTS:
        doc = uploaded_docs.get(doc_type)
        doc_checklist.append({
            'type': doc_type,
            'is_uploaded': doc is not None,
            'doc_data': doc
        })
        
    return render_template('student/documents.html', app=app_details, checklist=doc_checklist)

@docs_bp.route('/upload', methods=['POST'])
@student_required
def upload_document():
    user_id = session.get('user_id')
    apps = Application.find_by_student(user_id)
    if not apps:
        flash('Application record not found.', 'danger')
        return redirect(url_for('student.dashboard'))
        
    app_id = apps[0]['id']
    doc_type = request.form.get('document_type')
    file = request.files.get('file')
    
    if not file or file.filename == '':
        flash('No file selected for upload.', 'danger')
        return redirect(url_for('documents.manage_documents'))
        
    if file and allowed_file(file.filename):
        filename = secure_filename(f"APP_{app_id}_{doc_type.replace(' ', '_')}_{file.filename}")
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Add to database
        doc_id = DocumentModel.add(app_id, doc_type, file_path, filename)
        
        # Trigger OCR Processing automatically
        app_details = Application.get_full_details(app_id)
        ocr_result = process_document_ocr(file_path, doc_type, app_details.get('academic', {}))
        
        DocumentModel.update_verification(
            doc_id,
            ocr_result['verification_status'],
            ocr_result['message'],
            ocr_result['extracted_text']
        )
        
        # Check if all required docs uploaded
        updated_docs = DocumentModel.get_by_application(app_id)
        if len(updated_docs) >= len(REQUIRED_DOCUMENTS):
            Application.update_status(app_id, 'DOCUMENT_VERIFICATION')
            
        flash(f'{doc_type} uploaded and OCR verified successfully!', 'success')
    else:
        flash('Invalid file format. Only PDF, JPG, JPEG, PNG are allowed.', 'danger')
        
    return redirect(url_for('documents.manage_documents'))

@docs_bp.route('/digilocker-verify', methods=['POST'])
@student_required
def digilocker_verify():
    user_id = session.get('user_id')
    apps = Application.find_by_student(user_id)
    if not apps:
        return jsonify({'success': False, 'message': 'Application not found.'})
        
    app_id = apps[0]['id']
    doc_type = request.json.get('document_type', 'Class 12 Marksheet')
    
    # Check if doc exists in DB or create virtual record
    existing_docs = DocumentModel.get_by_application(app_id)
    matching_doc = next((d for d in existing_docs if d['document_type'] == doc_type), None)
    
    if matching_doc:
        DocumentModel.update_verification(
            matching_doc['id'],
            'VERIFIED',
            'Authenticity confirmed via DigiLocker Prototype API',
            ocr_text="[DIGILOCKER VERIFIED] Record matched with Central Academic Depository.",
            is_digilocker=1
        )
    else:
        # Create virtual verified document entry
        DocumentModel.add(
            app_id, doc_type,
            file_path="digilocker_verified_stub",
            file_name=f"digilocker_{doc_type.replace(' ', '_')}.pdf",
            ocr_text="[DIGILOCKER VERIFIED DEMO] Record fetched from Central Academic Repository.",
            verification_status="VERIFIED",
            verification_message="Verified via DigiLocker Prototype Simulation",
            is_digilocker=1
        )
        
    return jsonify({
        'success': True,
        'message': f'{doc_type} successfully verified via DigiLocker Prototype!',
        'status': 'DIGILOCKER VERIFIED'
    })

@docs_bp.route('/delete/<int:doc_id>', methods=['POST'])
@student_required
def delete_document(doc_id):
    DocumentModel.delete(doc_id)
    flash('Document deleted.', 'info')
    return redirect(url_for('documents.manage_documents'))
