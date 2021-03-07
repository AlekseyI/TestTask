import sqlalchemy as sqla
from datetime import datetime
from app.base import db


class Task(db.Model):
    id = sqla.Column(sqla.Integer(), primary_key=True)
    lower_limit = sqla.Column(sqla.Float(), nullable=False, default=0)
    upper_limit = sqla.Column(sqla.Float(), nullable=False, default=0)
    task_results = db.relationship('TaskResult', backref=db.backref('task'), lazy='dynamic', cascade='all,delete')
    created_on = sqla.Column(sqla.DateTime(), default=datetime.utcnow)
    updated_on = sqla.Column(sqla.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<{} : {}, {}, {}, {}>'.format(Task.__name__, self.id, self.lower_limit, self.upper_limit, self.created_on)


class TaskResult(db.Model):
    id = sqla.Column(sqla.Integer(), primary_key=True)
    params = sqla.Column(sqla.JSON(), nullable=False)
    result = sqla.Column(sqla.Float(), nullable=False, default=0)
    task_id = sqla.Column(sqla.Integer(), sqla.ForeignKey('task.id'), nullable=False)
    user_id = sqla.Column(sqla.Integer(), sqla.ForeignKey('user.id'), nullable=False)
    created_on = sqla.Column(sqla.DateTime(), default=datetime.utcnow)
    updated_on = sqla.Column(sqla.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(TaskResult, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '{} : {} {} {} {}'.format(TaskResult.__name__, self.id, self.params, self.result, self.task_id)
