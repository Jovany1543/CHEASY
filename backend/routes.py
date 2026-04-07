from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from models import db, Teacher, Student, Course, Section, Assignment, Submission, Enrollment

api = Blueprint('api', __name__, url_prefix='/api')

USER_FIELDS = ('username', 'first_name', 'last_name', 'email', 'phone_number')


def apply_user_updates(user, data):
    for field in USER_FIELDS:
        if field in data:
            setattr(user, field, data[field])


def validate_unique_user_fields(model, data, current_id=None):
    username = data.get('username')
    if username:
        existing_user = model.query.filter_by(username=username).first()
        if existing_user and existing_user.id != current_id:
            return jsonify({'msg': 'Username already exists'}), 409

    email = data.get('email')
    if email:
        existing_email = model.query.filter_by(email=email).first()
        if existing_email and existing_email.id != current_id:
            return jsonify({'msg': 'Email already exists'}), 409

    return None


def build_access_token(user_id, role):
    return create_access_token(
        identity=str(user_id),
        additional_claims={
            'user_id': user_id,
            'role': role,
        },
    )

# ===============================
# AUTH
# ===============================

@api.route('/teacher/login', methods=['POST'])
def teacher_login():
    data = request.get_json()
    teacher = Teacher.query.filter_by(username=data.get('username')).first()
    if teacher and teacher.check_password(data.get('password')):
        token = build_access_token(teacher.id, 'teacher')
        return jsonify(access_token=token), 200
    return jsonify({'msg': 'Invalid credentials'}), 401

@api.route('/student/login', methods=['POST'])
def student_login():
    data = request.get_json()
    student = Student.query.filter_by(username=data.get('username')).first()
    if student and student.check_password(data.get('password')):
        token = build_access_token(student.id, 'student')
        return jsonify(access_token=token), 200
    return jsonify({'msg': 'Invalid credentials'}), 401

# ===============================
# TEACHERS
# ===============================

@api.route('/teachers', methods=['GET'])
@jwt_required()
def get_teachers():
    teachers = Teacher.query.all()
    return jsonify([t.to_dict() for t in teachers]), 200

@api.route('/teachers/<int:id>', methods=['GET'])
@jwt_required()
def get_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    return jsonify(teacher.to_dict()), 200

@api.route('/teachers', methods=['POST'])
def create_teacher():
    data = request.get_json()
    validation_error = validate_unique_user_fields(Teacher, data)
    if validation_error:
        return validation_error

    teacher = Teacher(username=data['username'])
    apply_user_updates(teacher, data)
    teacher.set_password(data['password'])
    db.session.add(teacher)
    db.session.commit()
    return jsonify(teacher.to_dict()), 201

@api.route('/teachers/<int:id>', methods=['PUT'])
@jwt_required()
def update_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    data = request.get_json()
    validation_error = validate_unique_user_fields(Teacher, data, current_id=teacher.id)
    if validation_error:
        return validation_error

    apply_user_updates(teacher, data)
    if 'password' in data:
        teacher.set_password(data['password'])
    db.session.commit()
    return jsonify(teacher.to_dict()), 200

@api.route('/teachers/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()
    return jsonify({'msg': 'Teacher deleted'}), 200

# ===============================
# STUDENTS
# ===============================

@api.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students]), 200

@api.route('/students/<int:id>', methods=['GET'])
@jwt_required()
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify(student.to_dict()), 200

@api.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    validation_error = validate_unique_user_fields(Student, data)
    if validation_error:
        return validation_error

    student = Student(username=data['username'])
    apply_user_updates(student, data)
    student.set_password(data['password'])
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201

@api.route('/students/<int:id>', methods=['PUT'])
@jwt_required()
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json()
    validation_error = validate_unique_user_fields(Student, data, current_id=student.id)
    if validation_error:
        return validation_error

    apply_user_updates(student, data)
    if 'password' in data:
        student.set_password(data['password'])
    db.session.commit()
    return jsonify(student.to_dict()), 200

@api.route('/students/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'msg': 'Student deleted'}), 200

# ===============================
# COURSES
# ===============================

@api.route('/courses', methods=['GET'])
@jwt_required()
def get_courses():
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses]), 200

@api.route('/courses/<int:id>', methods=['GET'])
@jwt_required()
def get_course(id):
    course = Course.query.get_or_404(id)
    return jsonify(course.to_dict()), 200

@api.route('/courses', methods=['POST'])
@jwt_required()
def create_course():
    data = request.get_json()
    course = Course(
        name=data['name'],
        description=data.get('description'),
    )
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_dict()), 201

@api.route('/courses/<int:id>', methods=['PUT'])
@jwt_required()
def update_course(id):
    course = Course.query.get_or_404(id)
    data = request.get_json()
    if 'name' in data:
        course.name = data['name']
    if 'description' in data:
        course.description = data['description']
    db.session.commit()
    return jsonify(course.to_dict()), 200

@api.route('/courses/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'msg': 'Course deleted'}), 200

# ===============================
# SECTIONS
# ===============================

@api.route('/sections', methods=['GET'])
@jwt_required()
def get_sections():
    sections = Section.query.all()
    return jsonify([s.to_dict() for s in sections]), 200

@api.route('/sections/<int:id>', methods=['GET'])
@jwt_required()
def get_section(id):
    section = Section.query.get_or_404(id)
    return jsonify(section.to_dict()), 200

@api.route('/sections', methods=['POST'])
@jwt_required()
def create_section():
    data = request.get_json()
    Course.query.get_or_404(data['course_id'])  # validate course exists
    section = Section(
        name=data['name'],
        description=data['description'],
        course_id=data['course_id'],
    )
    db.session.add(section)
    db.session.commit()
    return jsonify(section.to_dict()), 201

@api.route('/sections/<int:id>', methods=['PUT'])
@jwt_required()
def update_section(id):
    section = Section.query.get_or_404(id)
    data = request.get_json()
    if 'name' in data:
        section.name = data['name']
    if 'description' in data:
        section.description = data['description']
    if 'course_id' in data:
        Course.query.get_or_404(data['course_id'])
        section.course_id = data['course_id']
    db.session.commit()
    return jsonify(section.to_dict()), 200

@api.route('/sections/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_section(id):
    section = Section.query.get_or_404(id)
    db.session.delete(section)
    db.session.commit()
    return jsonify({'msg': 'Section deleted'}), 200

# ===============================
# ASSIGNMENTS
# ===============================

@api.route('/assignments', methods=['GET'])
@jwt_required()
def get_assignments():
    assignments = Assignment.query.all()
    return jsonify([a.to_dict() for a in assignments]), 200

@api.route('/assignments/<int:id>', methods=['GET'])
@jwt_required()
def get_assignment(id):
    assignment = Assignment.query.get_or_404(id)
    return jsonify(assignment.to_dict()), 200

@api.route('/assignments', methods=['POST'])
@jwt_required()
def create_assignment():
    data = request.get_json()
    Section.query.get_or_404(data['section_id'])
    assignment = Assignment(
        title=data['title'],
        description=data.get('description'),
        section_id=data['section_id']
    )
    db.session.add(assignment)
    db.session.commit()
    return jsonify(assignment.to_dict()), 201

@api.route('/assignments/<int:id>', methods=['PUT'])
@jwt_required()
def update_assignment(id):
    assignment = Assignment.query.get_or_404(id)
    data = request.get_json()
    if 'title' in data:
        assignment.title = data['title']
    if 'description' in data:
        assignment.description = data['description']
    if 'section_id' in data:
        Section.query.get_or_404(data['section_id'])
        assignment.section_id = data['section_id']
    db.session.commit()
    return jsonify(assignment.to_dict()), 200

@api.route('/assignments/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_assignment(id):
    assignment = Assignment.query.get_or_404(id)
    db.session.delete(assignment)
    db.session.commit()
    return jsonify({'msg': 'Assignment deleted'}), 200

# ===============================
# SUBMISSIONS
# ===============================

@api.route('/submissions', methods=['GET'])
@jwt_required()
def get_submissions():
    submissions = Submission.query.all()
    return jsonify([s.to_dict() for s in submissions]), 200

@api.route('/submissions/<int:id>', methods=['GET'])
@jwt_required()
def get_submission(id):
    submission = Submission.query.get_or_404(id)
    return jsonify(submission.to_dict()), 200

@api.route('/submissions', methods=['POST'])
@jwt_required()
def create_submission():
    data = request.get_json()
    Student.query.get_or_404(data['student_id'])
    Assignment.query.get_or_404(data['assignment_id'])
    submission = Submission(
        student_id=data['student_id'],
        assignment_id=data['assignment_id'],
        content=data['content']
    )
    db.session.add(submission)
    db.session.commit()
    return jsonify(submission.to_dict()), 201

@api.route('/submissions/<int:id>', methods=['PUT'])
@jwt_required()
def update_submission(id):
    submission = Submission.query.get_or_404(id)
    data = request.get_json()
    if 'content' in data:
        submission.content = data['content']
    if 'grade' in data:
        submission.grade = data['grade']
    db.session.commit()
    return jsonify(submission.to_dict()), 200

@api.route('/submissions/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_submission(id):
    submission = Submission.query.get_or_404(id)
    db.session.delete(submission)
    db.session.commit()
    return jsonify({'msg': 'Submission deleted'}), 200

# ===============================
# ENROLLMENTS
# ===============================

@api.route('/enrollments', methods=['GET'])
@jwt_required()
def get_enrollments():
    enrollments = Enrollment.query.all()
    return jsonify([e.to_dict() for e in enrollments]), 200

@api.route('/enrollments/<int:id>', methods=['GET'])
@jwt_required()
def get_enrollment(id):
    enrollment = Enrollment.query.get_or_404(id)
    return jsonify(enrollment.to_dict()), 200

@api.route('/enrollments', methods=['POST'])
@jwt_required()
def create_enrollment():
    data = request.get_json()
    Teacher.query.get_or_404(data['teacher_id'])
    Student.query.get_or_404(data['student_id'])
    Course.query.get_or_404(data['course_id'])
    enrollment = Enrollment(
        teacher_id=data['teacher_id'],
        student_id=data['student_id'],
        course_id=data['course_id']
    )
    db.session.add(enrollment)
    db.session.commit()
    return jsonify(enrollment.to_dict()), 201

@api.route('/enrollments/<int:id>', methods=['PUT'])
@jwt_required()
def update_enrollment(id):
    enrollment = Enrollment.query.get_or_404(id)
    data = request.get_json()
    if 'teacher_id' in data:
        Teacher.query.get_or_404(data['teacher_id'])
        enrollment.teacher_id = data['teacher_id']
    if 'student_id' in data:
        Student.query.get_or_404(data['student_id'])
        enrollment.student_id = data['student_id']
    if 'course_id' in data:
        Course.query.get_or_404(data['course_id'])
        enrollment.course_id = data['course_id']
    db.session.commit()
    return jsonify(enrollment.to_dict()), 200

@api.route('/enrollments/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_enrollment(id):
    enrollment = Enrollment.query.get_or_404(id)
    db.session.delete(enrollment)
    db.session.commit()
    return jsonify({'msg': 'Enrollment deleted'}), 200