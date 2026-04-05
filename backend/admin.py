from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import Flask, redirect, request, abort
import os

class PasswordProtectedAdminIndexView(AdminIndexView):
    def is_accessible(self):
        # Check if user is authenticated via session
        return request.remote_addr == '127.0.0.1' or 'admin_authenticated' in request.cookies

    def _handle_view(self, name, **kwargs):
        # Redirect unauthenticated users to login
        if not self.is_accessible():
            return redirect('/admin-login')
        return super()._handle_view(name, **kwargs)

class ProtectedModelView(ModelView):
    def is_accessible(self):
        return request.remote_addr == '127.0.0.1' or 'admin_authenticated' in request.cookies

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect('/admin-login')
        return super()._handle_view(name, **kwargs)


def init_admin(app, db, Teacher, Student, Course, Section, Assignment, Submission, Enrollment):
    admin = Admin(app, name='CHEASY Admin', index_view=PasswordProtectedAdminIndexView())
    admin.add_view(ProtectedModelView(Teacher, db.session, name='Teachers'))
    admin.add_view(ProtectedModelView(Student, db.session, name='Students'))
    admin.add_view(ProtectedModelView(Course, db.session, name='Courses'))
    admin.add_view(ProtectedModelView(Section, db.session, name='Sections'))
    admin.add_view(ProtectedModelView(Assignment, db.session, name='Assignments'))
    admin.add_view(ProtectedModelView(Submission, db.session, name='Submissions'))
    admin.add_view(ProtectedModelView(Enrollment, db.session, name='Enrollments'))
    return admin
