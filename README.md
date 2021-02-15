**Create file .env in root dir task**

**Example content .env**

SECRET_KEY=af92d9da-8da0-4375-85ed-da23e60c57c6

POSTGRES_USER=postgres

POSTGRES_PASSWORD=postgres

POSTGRES_DB=test_db

POSTGRES_HOST=postgres_db:5432

DEBUG=True

SQLALCHEMY_TRACK_MODIFICATIONS=False

**Command to start project:**

`docker-compose up -d postgres_db`

`docker-compose up -d web`

