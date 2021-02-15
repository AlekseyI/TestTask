from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username ', validators=[DataRequired()])
    password = PasswordField('Password ', validators=[DataRequired()])
    remember = BooleanField('Remember Me ')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username ', validators=[DataRequired()])
    password = PasswordField('Password ', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password ', validators=[DataRequired()])
    submit = SubmitField('Registration')
