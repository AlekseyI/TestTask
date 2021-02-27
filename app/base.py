from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_script import Manager
from celery import Celery

app = Flask(__name__)
celery = Celery(__name__)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
admin = Admin()
migrate = Migrate(app, db)
manager = Manager(app)
