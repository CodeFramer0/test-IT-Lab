#!/bin/sh
set -e

echo "Applying migrations..."
poetry run python manage.py makemigrations --noinput
poetry run python manage.py makemigrations todo --noinput
poetry run python manage.py migrate --noinput

echo "Collecting static files..."
poetry run python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec poetry run gunicorn core.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 5 \
  --threads 5 \
  --worker-class gthread \
  --timeout 60 \
  --max-requests 1000 \
  --max-requests-jitter 50
