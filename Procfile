release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn mysite.wsgi --bind 0.0.0.0:$PORT
