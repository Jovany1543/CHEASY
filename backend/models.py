
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

# ===============================
# USER MODELS
# ===============================

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Teacher {self.id}: {self.username}>'

    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'first_name': self.first_name, 'last_name': self.last_name, 'email': self.email, 'phone_number': self.phone_number}

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Student {self.id}: {self.username}>'

    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'first_name': self.first_name, 'last_name': self.last_name, 'email': self.email, 'phone_number': self.phone_number}

# ===============================
# COURSE STRUCTURE MODELS
# ===============================

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Course {self.name}>'

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'description': self.description}
    
class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    course = db.relationship('Course', backref=db.backref('sections', lazy=True))

    def __repr__(self):
        return f'<Section {self.id}: {self.name}>'

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'course_id': self.course_id}
    
class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)

    section = db.relationship('Section', backref=db.backref('assignments', lazy=True))

    def __repr__(self):
        return f'<Assignment {self.id}: {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'section_id': self.section_id
        }

# ===============================
# ACTIVITY MODELS
# ===============================

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    grade = db.Column(db.String(10), nullable=True)

    student = db.relationship('Student', backref=db.backref('submissions', lazy=True))
    assignment = db.relationship('Assignment', backref=db.backref('submissions', lazy=True))

    def __repr__(self):
        return f'<Submission {self.id}: student={self.student_id} assignment={self.assignment_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'assignment_id': self.assignment_id,
            'content': self.content,
            'submission_date': self.submission_date.isoformat(),
            'grade': self.grade
        }

    
class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)

    teacher = db.relationship('Teacher', backref=db.backref('enrollments', lazy=True))
    student = db.relationship('Student', backref=db.backref('enrollments', lazy=True))
    course = db.relationship('Course', backref=db.backref('enrollments', lazy=True))

    def __repr__(self):
        return f'<Enrollment {self.id}: teacher={self.teacher_id} student={self.student_id} course={self.course_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'enrollment_date': self.enrollment_date.isoformat()
        }
