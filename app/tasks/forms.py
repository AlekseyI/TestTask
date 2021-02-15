from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    lower_limit = FloatField('Lower Limit ', validators=[DataRequired()])
    upper_limit = FloatField('Upper Limit ', validators=[DataRequired()])
    users = SelectMultipleField('Users ', choices=[(0, None)], coerce=int, default=[0])
    create_submit = SubmitField('Create')
    update_submit = SubmitField('Update')
    delete_submit = SubmitField('Delete')
    back_submit = SubmitField('Back')
