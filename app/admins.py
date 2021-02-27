from flask_admin import AdminIndexView
from flask_admin import expose
from flask_admin.contrib import sqla
from flask_login import current_user, logout_user
from flask import abort, redirect, url_for


class AdminPermissions:

    def is_accessible(self):
        return current_user.is_authenticated and current_user.active and current_user.superuser

    def inaccessible_callback(self, name, **kwargs):
        return abort(404)


class AdminHomeView(AdminPermissions, AdminIndexView):

    @expose('/')
    def index(self):
        return super(AdminHomeView, self).index()

    @expose('/logout/')
    def logout(self):
        logout_user()
        return redirect(url_for('index'))


class TaskAdminView(AdminPermissions, sqla.ModelView):
    form_excluded_columns = ['task_results', 'created_on', 'updated_on']


class UserAdminView(AdminPermissions, sqla.ModelView):
    form_excluded_columns = ['tasks_results', 'created_on', 'updated_on']
    column_exclude_list = ['password']

    def on_model_change(self, form, model, is_created):
        model.set_password(model.password)
        return super(UserAdminView, self).on_model_change(form, model, is_created)


class TaskResultAdminView(AdminPermissions, sqla.ModelView):
    column_list = ['id', 'params', 'result', 'task_id', 'user_id', 'created_on', 'updated_on']
    column_exclude_list = ['task_id', 'user_id']
    can_create = False
    can_edit = False
