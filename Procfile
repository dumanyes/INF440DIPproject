web: gunicorn INF440assign.wsgi --log-file -
#or works good with external database
web: python manage.py migrate && gunicorn INF440assign.wsgi
