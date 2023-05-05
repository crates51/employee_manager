#!/bin/bash

echo "Waiting for postgres..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py migrate
python manage.py createsuperuser --noinput # This line is for testing purposes, not intented for production
python manage.py loaddata app/seed/employees.json
python manage.py runserver 0.0.0.0:8000
