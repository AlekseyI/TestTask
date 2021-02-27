import os
from dotenv import load_dotenv
import ast

app_dir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(app_dir, '.env')
load_dotenv(env_path)


def generate_connect(key, driver, username, password, host, path):
    connect = '{}://{}:{}@{}/{}'.format(driver, username, password, host, path)
    os.environ[key] = connect
    return connect


class Config:
    SECRET_KEY = os.environ['SECRET_KEY']
    FLASK_ADMIN_SWATCH = 'cerulean'
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
    DEBUG = os.environ['DEBUG']
    SQLALCHEMY_DATABASE_URI = generate_connect('SQLALCHEMY_DATABASE_URI',
                                               'postgresql',
                                               os.environ['POSTGRES_USER'],
                                               os.environ['POSTGRES_PASSWORD'],
                                               os.environ['POSTGRES_HOST'],
                                               os.environ['POSTGRES_DB'])

    RABBITMQ_USERNAME = os.environ['RABBITMQ_USERNAME']
    RABBITMQ_PASSWORD = os.environ['RABBITMQ_PASSWORD']
    RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
    RABBITMQ_VHOST = os.environ['RABBITMQ_VHOST']

    CELERY_BROKER_URL = generate_connect('CELERY_BROKER_URL',
                                         'amqp',
                                         os.environ['RABBITMQ_USERNAME'],
                                         os.environ['RABBITMQ_PASSWORD'],
                                         os.environ['RABBITMQ_HOST'],
                                         os.environ['RABBITMQ_VHOST'])

    CELERY_RESULT_BACKEND = generate_connect('CELERY_RESULT_BACKEND',
                                             'rpc',
                                             os.environ['RABBITMQ_USERNAME'],
                                             os.environ['RABBITMQ_PASSWORD'],
                                             os.environ['RABBITMQ_HOST'],
                                             os.environ['RABBITMQ_VHOST'])

    CELERY_ACCEPT_CONTENT = ast.literal_eval(os.environ['CELERY_ACCEPT_CONTENT'])
    CELERY_TASK_SERIALIZER = os.environ['CELERY_TASK_SERIALIZER']
    CELERY_RESULT_SERIALIZER = os.environ['CELERY_RESULT_SERIALIZER']
    CELERY_TIMEZONE = os.environ['CELERY_TIMEZONE']
    GENERATE_RANDOM_NUMBER_TASK = int(os.environ['GENERATE_RANDOM_NUMBER_TASK'])
