from celery import group
from random import randint
from app.tasks.models import TaskResult
from app.models import User
from app.base import celery
from app.base import db


@celery.task
def action_task(id):
    user = User.query.filter(User.id == id).first()
    count_tasks = len(user.tasks)
    if count_tasks == 0:
        return

    task = user.tasks[randint(0, count_tasks-1)]
    task_res = TaskResult(task_id=task.id, user_id=user.id)
    task_res.result = randint(task.lower_limit, task.upper_limit)
    task_res.params = {
        'author_id': task_res.user_id,
        'lower_limit': task.lower_limit,
        'upper_limit': task.upper_limit
    }
    db.session.add(task_res)
    db.session.commit()


@celery.task
def task_generator():
    users = db.session.query(User.id).filter(User.superuser.is_(False)).all()
    group_tasks = group(action_task.s(user.id) for user in users)
    group_tasks.apply_async()
