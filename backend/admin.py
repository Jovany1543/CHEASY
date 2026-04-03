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

def init_admin(app, db, User, Item):
    admin = Admin(app, name='CHEASY Admin', index_view=PasswordProtectedAdminIndexView())
    admin.add_view(ProtectedModelView(User, db.session, name='Users'))
    admin.add_view(ProtectedModelView(Item, db.session, name='Items'))
    return admin
