**Create file .env in root dir**

**Example content .env**

SECRET_KEY=af92d9da-8da0-4375-85ed-da23e60c57c6

POSTGRES_USER=postgres

POSTGRES_PASSWORD=postgres

POSTGRES_DB=test_db

POSTGRES_HOST=postgres_db:5432

DEBUG=True

SQLALCHEMY_TRACK_MODIFICATIONS=False

CELERY_ACCEPT_CONTENT=["json"]

CELERY_TASK_SERIALIZER=json

CELERY_RESULT_SERIALIZER=json

CELERY_TIMEZONE=UTC

RABBITMQ_USERNAME=guest

RABBITMQ_PASSWORD=guest

RABBITMQ_VHOST=/

RABBITMQ_HOST=rabbit_mq:5672

GENERATE_RANDOM_NUMBER_TASK=300

**Command to start project:**

`docker-compose up -d postgres_db`

`docker-compose up -d rabbit_mq`

`docker-compose up -d web`

`docker-compose up -d celery_worker`

`docker-compose up -d celery_beat`

