import sqlalchemy as sqla
from datetime import datetime
from ..base import db


class Task(db.Model):
    id = sqla.Column(sqla.Integer(), primary_key=True)
    lower_limit = sqla.Column(sqla.Float(), nullable=False, default=0)
    upper_limit = sqla.Column(sqla.Float(), nullable=False, default=0)
    created_on = sqla.Column(sqla.DateTime(), default=datetime.utcnow)
    updated_on = sqla.Column(sqla.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<{} : {}, {}, {}, {}>'.format(Task.__name__, self.id, self.lower_limit, self.upper_limit, self.created_on)
