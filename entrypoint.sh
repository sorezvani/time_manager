#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

# Create a superuser if it doesn't exist
# This Python script is run inside the shell script
echo "Checking for superuser..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username='admin').exists():
    print("Creating superuser 'admin'")
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
else:
    print("Superuser 'admin' already exists")
EOF

# Start Gunicorn server
echo "Starting Gunicorn..."
exec "$@"