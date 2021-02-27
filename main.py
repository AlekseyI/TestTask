from app.app import init_app
from app.base import manager
from manager.worker import init_worker

app = init_app()
celery = init_worker()


if __name__ == '__main__':
    manager.run()
