#!/usr/bin/env bash
# Exit on error
set -o errexit

# Build script for Render deployment
python -m pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate --noinput

