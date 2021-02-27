from app.base import celery, app
from config import Config
from .tasks import task_generator


def init_worker():
    celery.conf.update(app.config)

    celery_task = celery.Task

    class ContextTask(celery_task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return celery_task.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(Config.GENERATE_RANDOM_NUMBER_TASK, task_generator.s())
