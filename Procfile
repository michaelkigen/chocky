web: gunicorn test_project.wsgi
release: python manage.py makemigrations --noinput
release: python manage.py migrate --noinput