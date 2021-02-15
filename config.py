import os
from dotenv import load_dotenv

app_dir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(app_dir, '.env')
load_dotenv(env_path)


class Config:
    SECRET_KEY = os.environ['SECRET_KEY']
    FLASK_ADMIN_SWATCH = 'cerulean'
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
    DEBUG = os.environ['DEBUG']
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(os.environ['POSTGRES_USER'],
                                                                os.environ['POSTGRES_PASSWORD'],
                                                                os.environ['POSTGRES_HOST'],
                                                                os.environ['POSTGRES_DB'])
