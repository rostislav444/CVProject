#!/bin/sh

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
# Try to use nc command to check if PostgreSQL is ready
if command -v nc >/dev/null 2>&1; then
  while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
  done
else
  # If nc is not available, use a simple sleep
  echo "nc command not found, sleeping for 10 seconds"
  sleep 10
fi
echo "PostgreSQL is up - continuing..."

# Apply database migrations
echo "Applying migrations..."
python manage.py migrate

# Load initial fixtures if needed
python manage.py loaddata apps/main/fixtures/sample_cvs.json

# Start server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000