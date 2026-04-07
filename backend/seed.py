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
                'description': 'Foundational kitchen skills, safety, and fast-paced service prep.',
                'sections': [
                    {
                        'name': 'Knife Skills',
                        'description': 'Practice cuts, prep sequencing, and safe station setup.',
                        'assignments': [
                            {
                                'title': 'Mise en Place Drill',
                                'description': 'Prepare ingredients for a three-course meal under a time limit.',
                            },
                            {
                                'title': 'Vegetable Precision Cuts',
                                'description': 'Submit a prep log and plated sample of core knife cuts.',
                            },
                        ],
                    },
                    {
                        'name': 'Stocks and Sauces',
                        'description': 'Build flavor using foundational stocks, roux, and pan sauces.',
                        'assignments': [
                            {
                                'title': 'Mother Sauce Tasting',
                                'description': 'Prepare one mother sauce and explain its derivatives.',
                            }
                        ],
                    },
                ],
            },
            {
                'name': 'Baking Basics',
                'description': 'Essential doughs, batters, fermentation, and oven technique.',
                'sections': [
                    {
                        'name': 'Bread Fundamentals',
                        'description': 'Mixing, proofing, shaping, and scoring bread dough.',
                        'assignments': [
                            {
                                'title': 'Bread Lab',
                                'description': 'Bake a basic loaf and document the process from mix to crumb.',
                            },
                            {
                                'title': 'Hydration Comparison',
                                'description': 'Compare two dough hydrations and submit observations.',
                            },
                        ],
                    },
                    {
                        'name': 'Pastry Basics',
                        'description': 'Creaming, lamination, and temperature control in pastry work.',
                        'assignments': [
                            {
                                'title': 'Cookie Texture Study',
                                'description': 'Bake two cookie batches and explain the texture differences.',
                            }
                        ],
                    },
                ],
            },
            {
                'name': 'Global Flavors',
                'description': 'Ingredient pairing and technique across multiple culinary traditions.',
                'sections': [
                    {
                        'name': 'Spice Foundations',
                        'description': 'Toast, bloom, and layer spices for balanced dishes.',
                        'assignments': [
                            {
                                'title': 'Spice Blend Workshop',
                                'description': 'Create a custom spice blend and propose a dish around it.',
                            }
                        ],
                    },
                    {
                        'name': 'Regional Menu Design',
                        'description': 'Translate regional ingredients into a coherent small menu.',
                        'assignments': [
                            {
                                'title': 'Three-Course Menu Draft',
                                'description': 'Design a menu inspired by a single region and justify the pairings.',
                            }
                        ],
                    },
                ],
            },
        ]
        
        courses = []
        sections = []
        assignments = []
        course_assignments = {}
        for course_data in courses_data:
            course = Course(
                name=course_data['name'],
                description=course_data['description'],
            )
            db.session.add(course)
            db.session.flush()

            courses.append(course)
            course_assignments[course.id] = []

            for section_data in course_data['sections']:
                section = Section(
                    name=section_data['name'],
                    description=section_data['description'],
                    course_id=course.id,
                )
                db.session.add(section)
                db.session.flush()
                sections.append(section)

                for assignment_data in section_data['assignments']:
                    assignment = Assignment(
                        title=assignment_data['title'],
                        description=assignment_data['description'],
                        section_id=section.id,
                    )
                    assignments.append(assignment)
                    course_assignments[course.id].append(assignment)
                    db.session.add(assignment)
        
        db.session.commit()
        print(f"Created {len(courses)} courses")
        print(f"Created {len(sections)} sections")
        print(f"Created {len(assignments)} assignments")

        # Enroll students and add submissions
        print("Creating enrollments and submissions...")
        enrollments = []
        submissions = []
        sample_grades = ['A', 'A-', 'B+', 'B', None]
        for student_index, student in enumerate(students):
            for course_index, course in enumerate(courses):
                teacher = teachers[(student_index + course_index) % len(teachers)]

                enrollment = Enrollment(
                    teacher_id=teacher.id,
                    student_id=student.id,
                    course_id=course.id,
                )
                enrollments.append(enrollment)
                db.session.add(enrollment)

                for assignment_index, assignment in enumerate(course_assignments[course.id]):
                    submission = Submission(
                        student_id=student.id,
                        assignment_id=assignment.id,
                        content=(
                            f"{student.first_name} {student.last_name} completed {assignment.title} "
                            f"for {course.name}."
                        ),
                        grade=sample_grades[(student_index + assignment_index + course_index) % len(sample_grades)],
                    )

                    submissions.append(submission)
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
