from flask import render_template, Blueprint, redirect, url_for, flash, request, session
from flask_login import login_required, logout_user, current_user
from sqlalchemy import func, and_, or_
from .models import Task
from .forms import TaskForm
from app.models import User
from app.base import db


tasks = Blueprint('tasks', __name__, template_folder='templates')


@tasks.route('/')
@login_required
def index():
    if current_user.superuser:
        return redirect(url_for('tasks.list_tasks'))
    return render_template('task/index.html',
                           username=current_user.username,
                           tasks=current_user.tasks)


@tasks.route('/<name>')
@login_required
def view_user_tasks(name):
    if current_user.superuser or current_user.can_review_tasks:
        user = User.query.filter(User.username == name).filter(
            and_(User.active.is_(True), User.superuser.is_(False),
                 or_(current_user.superuser,
                     and_(User.can_review_tasks.is_(False), current_user.can_review_tasks))))
        if user.count() > 0:
            user = user.one()
        else:
            return redirect(url_for('tasks.index'))
        return render_template('task/index.html',
                               username=user.username,
                               tasks=user.tasks)
    return redirect(url_for('tasks.index'))


@tasks.route('/users_tasks/')
@login_required
def users_tasks():
    if current_user.superuser or current_user.can_review_tasks:
        users_and_tasks = db.session.query(User.username, User.can_review_tasks, func.count(Task.id))\
        .filter(and_(User.active.is_(True), User.superuser.is_(False),
            or_(current_user.superuser, and_(User.can_review_tasks.is_(False), current_user.can_review_tasks))))\
            .outerjoin(User.tasks).group_by(User.id).order_by(User.username).all()
        return render_template('task/users_tasks.html', users_and_tasks=users_and_tasks)
    return redirect(url_for('tasks.index'))


@tasks.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def preview(id):
    form = TaskForm()

    if 'last_url' not in session:
        session['last_url'] = request.referrer

    if form.back_submit.data:
        back_url = session['last_url']
        session.pop('last_url', None)
        if back_url is None:
            return redirect(url_for('index'))
        else:
            return redirect(back_url)

    task = Task.query.get(id)

    if form.delete_submit.data:
        for user in task.users:
            user.tasks.remove(task)
            db.session.add(user)
        db.session.delete(task)
        db.session.commit()
        back_url = session['last_url']
        session.pop('last_url', None)
        if back_url is None:
            return redirect(url_for('tasks.list_tasks'))
        else:
            return redirect(back_url)

    form.users.choices += db.session.query(User.id, User.username)\
        .filter(User.active.is_(True), User.superuser.is_(False))\
        .order_by(User.username)\
        .all()

    if form.validate_on_submit():
        lower_limit = form.lower_limit.data
        upper_limit = form.upper_limit.data
        choice_users = form.users.data

        if lower_limit < 0 or upper_limit < 0:
            flash('Low Limit and Upper Limit not be negative', 'error')
        elif lower_limit >= upper_limit:
            flash('Low Limit must be smaller then Upper Limit', 'error')
        else:

            task.lower_limit = lower_limit
            task.upper_limit = upper_limit

            try:
                choice_users.pop(choice_users.index(0))
            except ValueError:
                pass

            users_for_task = [user.id for user in task.users.all()]
            count_ch_user = len(choice_users)
            count_us_task = len(users_for_task)

            diff_user = list(set(choice_users) ^ set(users_for_task))

            if count_ch_user > 0 and count_us_task == 0:
                users = User.query.filter(User.id.in_(diff_user))
                for user in users:
                    user.tasks.append(task)
                    db.session.add(user)
            elif count_ch_user > 0 and count_us_task > 0:
                users = User.query.filter(User.id.in_(diff_user))
                if count_us_task > count_ch_user:
                    for user in users:
                        user.tasks.remove(task)
                        db.session.add(user)
                else:
                    for user in users:
                        user.tasks.append(task)
                        db.session.add(user)
            else:
                for user in task.users:
                    user.tasks.remove(task)
                    db.session.add(user)
            db.session.commit()

    form.lower_limit.data = task.lower_limit
    form.upper_limit.data = task.upper_limit

    users_for_task = task.users.all()
    if len(users_for_task) > 0:
        form.users.data = [user.id for user in users_for_task]
    else:
        form.users.data = form.users.default

    return render_template('task/preview.html', task=task, form=form)


@tasks.route('/list_tasks/')
@login_required
def list_tasks():
    if not current_user.superuser:
        return redirect(url_for('tasks.index'))
    tasks = Task.query.order_by(Task.id).all()
    return render_template('task/list_tasks.html', tasks=tasks)


@tasks.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    if not current_user.superuser:
        return redirect(url_for('tasks.index'))

    form = TaskForm()

    if 'last_url' not in session:
        session['last_url'] = request.referrer

    if form.back_submit.data:
        back_url = session['last_url']
        session.pop('last_url', None)
        if back_url is None:
            return redirect(url_for('tasks.list_tasks'))
        else:
            return redirect(back_url)

    form.users.choices += db.session.query(User.id, User.username)\
        .filter(User.active.is_(True) & User.superuser.is_(False))\
        .order_by(User.username)\
        .all()

    if form.validate_on_submit():
        lower_limit = form.lower_limit.data
        upper_limit = form.upper_limit.data
        choice_users = form.users.data

        if lower_limit < 0 or upper_limit < 0:
            flash('Low Limit and Upper Limit not be negative', 'error')
        elif lower_limit >= upper_limit:
            flash('Low Limit must be smaller then Upper Limit', 'error')
        else:
            task = Task(lower_limit=lower_limit, upper_limit=upper_limit)
            db.session.add(task)

            try:
                choice_users.pop(choice_users.index(0))
            except ValueError:
                pass

            if len(choice_users) > 0:
                users = User.query.filter(User.id.in_(choice_users))
                for user in users:
                    user.tasks.append(task)
                    db.session.add(user)
            db.session.commit()
        return redirect(url_for('tasks.create'))
    return render_template('task/create.html', form=form)


@tasks.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
