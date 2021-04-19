#!/bin/sh

# Prepare DB
python manage.py makemigrations
python manage.py migrate
python manage.py syncdb

# Start gunicorn server
gunicorn -c "allure_server/gunicorn.py" allure_server.wsgi

