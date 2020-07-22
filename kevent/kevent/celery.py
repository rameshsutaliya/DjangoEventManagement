import os
from celery import Celery
from celery.schedules import crontab
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kevent.settings')
app = Celery('kevent')
app.config_from_object('django.conf:settings')

#app.config_from_object('django.conf:settings',namespace='CELERY')

# Load task modules from all registered Django app configs.


app.autodiscover_tasks()

#Here register the periodic task
app.conf.beat_schedule ={
	'send-report-every-hour-minute':{
		'task':'core.tasks.trigger_emails',
		'schedule':crontab(minute='0',hour='*/1'),
	},
}

