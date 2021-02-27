from flask_migrate import MigrateCommand
from .admins import UserAdminView, TaskAdminView, TaskResultAdminView, AdminHomeView
from .models import get_user, User
from .views import login
from .base import db, admin, login_manager, manager, app
from .tasks.models import Task, TaskResult
from .tasks.views import tasks
from config import Config


def init_app():
    app.config.from_object(Config())
    init_admin()
    init_views()
    init_login()
    init_manager()
    return app


def init_admin():
    admin.init_app(app, AdminHomeView(name='Home'))
    admin.url = '/admin/'
    admin.base_template = 'admin/index.html'
    admin.add_view(UserAdminView(User, db.session))
    admin.add_view(TaskAdminView(Task, db.session))
    admin.add_view(TaskResultAdminView(TaskResult, db.session))


def init_login():
    login_manager.user_loader(get_user)
    login_manager.login_view = login.__name__


def init_views():
    app.register_blueprint(tasks, url_prefix='/task')


def init_manager():
    manager.add_command('db', MigrateCommand)
