#!/bin/bash

python main.py db upgrade
python main.py create_superuser admin admin
gunicorn gunicorn --bind :5000 main:app --log-level error --access-logfile /tmp/access.log --error-logfile /tmp/error.log