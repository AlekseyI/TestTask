from app.app import init_app
from app.base import manager

app = init_app()

if __name__ == '__main__':
    manager.run()
