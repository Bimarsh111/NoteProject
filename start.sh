#!/bin/bash

# Activate virtual environment (adjust path if needed)
source ../.venv/bin/activate

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the Gunicorn server
gunicorn base.wsgi:application --bind 0.0.0.0:8000
