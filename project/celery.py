import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Create the Celery app
app = Celery('project')
app.conf.broker_url = os.environ.get('CELERY_BROKER_URL')

app.conf.broker_connection_retry_on_startup = True

# Use a string here to avoid serializing the configuration object
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')