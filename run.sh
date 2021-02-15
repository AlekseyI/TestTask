#!/bin/bash

python main.py db upgrade
python main.py create_superuser admin admin
gunicorn --bind :5000 main:app