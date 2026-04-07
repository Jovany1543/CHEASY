#!/usr/bin/env python
"""
Seed script to populate the database with dummy data for development.
Run with: pipenv run seed
"""

from app import app, db, create_db
from models import Assignment, Course, Enrollment, Section, Student, Submission, Teacher

def seed_database():
    """Populate the database with dummy classroom data."""
    
    with app.app_context():
        # Ensure tables exist
        create_db()
        
        # Clear existing data
        print("Clearing existing data...")
        db.session.query(Submission).delete()
        db.session.query(Enrollment).delete()
        db.session.query(Assignment).delete()
        db.session.query(Section).delete()
        db.session.query(Course).delete()
        db.session.query(Student).delete()
        db.session.query(Teacher).delete()
        db.session.commit()
        
        # Create dummy teachers
        print("Creating dummy teachers...")
        teachers_data = [
            {
                'username': 'chefmarco',
                'password': 'password123',
                'first_name': 'Marco',
                'last_name': 'Rossi',
                'email': 'marco@example.com',
                'phone_number': '555-0101',
            },
            {
                'username': 'chefana',
                'password': 'securepass456',
                'first_name': 'Ana',
                'last_name': 'Lopez',
                'email': 'ana@example.com',
                'phone_number': '555-0102',
            },
        ]
        
        teachers = []
        for teacher_data in teachers_data:
            teacher = Teacher(
                username=teacher_data['username'],
                first_name=teacher_data['first_name'],
                last_name=teacher_data['last_name'],
                email=teacher_data['email'],
                phone_number=teacher_data['phone_number'],
            )
            teacher.set_password(teacher_data['password'])
            teachers.append(teacher)
            db.session.add(teacher)
        
        db.session.commit()
        print(f"Created {len(teachers)} teachers")

        # Create dummy students
        print("Creating dummy students...")
        students_data = [
            {
                'username': 'alice',
                'password': 'password123',
                'first_name': 'Alice',
                'last_name': 'Nguyen',
                'email': 'alice@example.com',
                'phone_number': '555-0201',
            },
            {
                'username': 'bob',
                'password': 'securepass456',
                'first_name': 'Bob',
                'last_name': 'Carter',
                'email': 'bob@example.com',
                'phone_number': '555-0202',
            },
            {
                'username': 'charlie',
                'password': 'mypassword789',
                'first_name': 'Charlie',
                'last_name': 'Kim',
                'email': 'charlie@example.com',
                'phone_number': '555-0203',
            },
        ]

        students = []
        for student_data in students_data:
            student = Student(
                username=student_data['username'],
                first_name=student_data['first_name'],
                last_name=student_data['last_name'],
                email=student_data['email'],
                phone_number=student_data['phone_number'],
            )
            student.set_password(student_data['password'])
            students.append(student)
            db.session.add(student)

        db.session.commit()
        print(f"Created {len(students)} students")
        
        # Create courses, sections, and assignments
        print("Creating dummy courses...")
        courses_data = [
            {
                'name': 'Intro to Cooking',
                'description': 'Foundational kitchen skills and safety.',
                'section_name': 'Knife Skills',
                'section_description': 'Practice cuts, prep, and handling techniques.',
                'assignment_title': 'Mise en Place Drill',
                'assignment_description': 'Prepare ingredients for a three-course meal.',
            },
            {
                'name': 'Baking Basics',
                'description': 'Essential doughs, batters, and oven technique.',
                'section_name': 'Bread Fundamentals',
                'section_description': 'Mixing, proofing, and shaping bread dough.',
                'assignment_title': 'Bread Lab',
                'assignment_description': 'Bake a basic loaf and document the process.',
            },
        ]
        
        courses = []
        sections = []
        assignments = []
        for index, course_data in enumerate(courses_data):
            course = Course(
                name=course_data['name'],
                description=course_data['description'],
            )
            db.session.add(course)
            db.session.flush()

            section = Section(
                name=course_data['section_name'],
                description=course_data['section_description'],
                course_id=course.id,
            )
            assignment = Assignment(
                title=course_data['assignment_title'],
                description=course_data['assignment_description'],
                course_id=course.id,
            )

            courses.append(course)
            sections.append(section)
            assignments.append(assignment)
            db.session.add(section)
            db.session.add(assignment)
        
        db.session.commit()
        print(f"Created {len(courses)} courses")

        # Enroll students and add submissions
        print("Creating enrollments and submissions...")
        enrollments = []
        submissions = []
        for index, student in enumerate(students):
            course = courses[index % len(courses)]
            teacher = teachers[index % len(teachers)]
            assignment = assignments[index % len(assignments)]

            enrollment = Enrollment(
                teacher_id=teacher.id,
                student_id=student.id,
                course_id=course.id,
            )
            submission = Submission(
                student_id=student.id,
                assignment_id=assignment.id,
                content=f"Submission by {student.username} for {assignment.title}",
                grade='A' if index == 0 else None,
            )

            enrollments.append(enrollment)
            submissions.append(submission)
            db.session.add(enrollment)
            db.session.add(submission)

        db.session.commit()
        print(f"Created {len(enrollments)} enrollments")
        print(f"Created {len(submissions)} submissions")
        
        print("\n✅ Database seeded successfully!")
        print(f"Teachers: {', '.join([teacher.username for teacher in teachers])}")
        print(f"Students: {', '.join([student.username for student in students])}")
        print(f"Courses: {', '.join([course.name for course in courses])}")

if __name__ == '__main__':
    seed_database()
