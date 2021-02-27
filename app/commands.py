from app.models import User
from app.base import manager, db


@manager.command
def create_superuser(username, password):
    'Create superuser with args username and password'
    user = User.query.filter(User.username == username).first()
    if user is None:
        user = User(username=username, superuser=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print('superuser created')
    else:
        print('superuser with this username exists')
