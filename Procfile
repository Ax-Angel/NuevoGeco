web: gunicorn geco.wsgi --limit-request-line 8188 --log-file -
worker: celery worker --app=geco --loglevel=info
