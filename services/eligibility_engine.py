COURSE_ELIGIBILITY_RULES = {
    'B.Tech Computer Science & Engineering': {
        'min_class12_percentage': 60.0,
        'min_math': 60.0,
        'min_physics': 55.0,
        'min_chemistry': 50.0,
        'min_entrance_score': 70.0,
        'mandatory_subjects': ['Mathematics', 'Physics', 'Chemistry']
    },
    'B.Tech Information Technology': {
        'min_class12_percentage': 60.0,
        'min_math': 55.0,
        'min_physics': 50.0,
        'min_chemistry': 50.0,
        'min_entrance_score': 65.0,
        'mandatory_subjects': ['Mathematics', 'Physics', 'Chemistry']
    },
    'B.Tech Electronics & Communication': {
        'min_class12_percentage': 55.0,
        'min_math': 55.0,
        'min_physics': 50.0,
        'min_chemistry': 50.0,
        'min_entrance_score': 60.0,
        'mandatory_subjects': ['Mathematics', 'Physics', 'Chemistry']
    },
    'B.Tech Mechanical Engineering': {
        'min_class12_percentage': 55.0,
        'min_math': 50.0,
        'min_physics': 50.0,
        'min_chemistry': 50.0,
        'min_entrance_score': 55.0,
        'mandatory_subjects': ['Mathematics', 'Physics', 'Chemistry']
    },
    'B.Tech Electrical Engineering': {
        'min_class12_percentage': 55.0,
        'min_math': 50.0,
        'min_physics': 50.0,
        'min_chemistry': 50.0,
        'min_entrance_score': 55.0,
        'mandatory_subjects': ['Mathematics', 'Physics', 'Chemistry']
    }
}

def evaluate_eligibility(course_name, academic_data):
    """
    Evaluates applicant's academic info against rule-based criteria for selected course.
    Returns boolean status and detailed check list.
    """
    rules = COURSE_ELIGIBILITY_RULES.get(course_name, COURSE_ELIGIBILITY_RULES['B.Tech Computer Science & Engineering'])
    
    checks = []
    is_eligible = True
    
    # 1. Class 12 Percentage Check
    class12 = float(academic_data.get('class12_percentage', 0))
    min_c12 = rules['min_class12_percentage']
    c12_passed = class12 >= min_c12
    if not c12_passed: is_eligible = False
    checks.append({
        'criterion': 'Class 12 Percentage',
        'student_value': f"{class12:.1f}%",
        'required_value': f"≥ {min_c12:.1f}%",
        'status': 'PASSED' if c12_passed else 'FAILED',
        'passed': c12_passed
    })
    
    # 2. Mathematics Score Check
    math_score = float(academic_data.get('mathematics', 0))
    min_math = rules['min_math']
    math_passed = math_score >= min_math
    if not math_passed: is_eligible = False
    checks.append({
        'criterion': 'Mathematics Score',
        'student_value': f"{math_score:.1f}",
        'required_value': f"≥ {min_math:.1f} (Mandatory)",
        'status': 'PASSED' if math_passed else 'FAILED',
        'passed': math_passed
    })
    
    # 3. Physics Score Check
    physics_score = float(academic_data.get('physics', 0))
    min_phys = rules['min_physics']
    phys_passed = physics_score >= min_phys
    if not phys_passed: is_eligible = False
    checks.append({
        'criterion': 'Physics Score',
        'student_value': f"{physics_score:.1f}",
        'required_value': f"≥ {min_phys:.1f} (Mandatory)",
        'status': 'PASSED' if phys_passed else 'FAILED',
        'passed': phys_passed
    })
    
    # 4. Chemistry Score Check
    chem_score = float(academic_data.get('chemistry', 0))
    min_chem = rules['min_chemistry']
    chem_passed = chem_score >= min_chem
    if not chem_passed: is_eligible = False
    checks.append({
        'criterion': 'Chemistry / Equivalent Score',
        'student_value': f"{chem_score:.1f}",
        'required_value': f"≥ {min_chem:.1f} (Mandatory)",
        'status': 'PASSED' if chem_passed else 'FAILED',
        'passed': chem_passed
    })
    
    # 5. Entrance Exam Score Check
    entrance_score = float(academic_data.get('entrance_score', 0))
    min_entrance = rules['min_entrance_score']
    entrance_passed = entrance_score >= min_entrance
    if not entrance_passed: is_eligible = False
    checks.append({
        'criterion': f"Entrance Score ({academic_data.get('entrance_exam', 'Entrance')})",
        'student_value': f"{entrance_score:.1f}",
        'required_value': f"≥ {min_entrance:.1f}",
        'status': 'PASSED' if entrance_passed else 'FAILED',
        'passed': entrance_passed
    })
    
    summary = {
        'course': course_name,
        'overall_status': 'ELIGIBLE' if is_eligible else 'NOT ELIGIBLE',
        'is_eligible': is_eligible,
        'checks': checks,
        'failed_criteria_count': sum(1 for c in checks if not c['passed'])
    }
    
    return is_eligible, summary
