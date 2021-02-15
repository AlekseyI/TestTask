from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user
from .forms import LoginForm, RegistrationForm
from .base import db, app
from .models import User


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('tasks.index'))
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('tasks.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('tasks.index'))
        else:
            flash('Username or Password Invalid', 'error')
    return render_template('login.html', form=form)


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('tasks.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        password = form.password.data
        repeat_password = form.repeat_password.data
        if password == repeat_password:
            user = User.query.filter(User.username == form.username.data).first()
            if user is None:
                user = User(username=form.username.data)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                flash('User with this username already register, use another', 'error')
        else:
            flash('Password and Repeat Password not equal', 'error')
    return render_template('registration.html', form=form)
