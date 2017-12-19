from celery import Celery
from . import settings

app = Celery('pipeline', broker='redis://localhost')
app.config_from_object(settings)
