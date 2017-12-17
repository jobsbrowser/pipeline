from celery import Celery

app = Celery('pipeline', broker='redis://localhost')
