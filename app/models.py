from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sqla
from flask_login import UserMixin
from datetime import datetime
from .base import db
from config import Config


user_task = db.Table(
    'user_task',
    sqla.Column('user_id', sqla.Integer(), sqla.ForeignKey('user.id')),
    sqla.Column('task_id', sqla.Integer(), sqla.ForeignKey('task.id')))


class User(db.Model, UserMixin):
    id = sqla.Column(sqla.Integer(), primary_key=True)
    username = sqla.Column(sqla.String(50), nullable=False, unique=True)
    password = sqla.Column(sqla.String(100), nullable=False)
    active = sqla.Column(sqla.Boolean(), nullable=False, default=True)
    superuser = sqla.Column(sqla.Boolean(), nullable=False, default=False)
    can_review_tasks = sqla.Column(sqla.Boolean(), nullable=False, default=False)
    tasks = db.relationship('Task', secondary=user_task, backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
    tasks_results = db.relationship('TaskResult', backref=db.backref('user'), lazy='dynamic', cascade='all,delete')
    created_on = sqla.Column(sqla.DateTime(), default=datetime.utcnow)
    updated_on = sqla.Column(sqla.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<{} : {}, {}, {}, {}>'.format(User.__name__, self.id, self.username, self.active, self.superuser)

    def set_password(self, password):
        self.password = generate_password_hash(password + Config.SECRET_KEY)

    def check_password(self, password):
        return check_password_hash(self.password, password + Config.SECRET_KEY)

    def __unicode__(self):
        return self.username


def get_user(user_id):
    return User.query.filter(User.id == user_id, User.active).first()
