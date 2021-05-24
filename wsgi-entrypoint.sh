#!/bin/sh

until cd /app
do
    echo "Waiting for server volume..."
done

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

echo "Starting collectstatic"
python manage.py collectstatic --noinput

echo "Starting server"
gunicorn freelance.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4
