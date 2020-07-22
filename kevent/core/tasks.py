import logging
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from celery.decorators import task

@task
def send_verification_email(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        send_mail(
            'Verify your KIITEvent account and after reset the Password ',
            'Follow this link to verify your account: '
                'http://localhost:8000%s' % reverse('verify', kwargs={'uuid': str(user.verification_uuid)}),
            'rameshsutliya@gmail.com',
            [user.email],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)
        

from event.models import Event
from datetime import datetime

def email_content(event,user):
	pass


@task
def trigger_emails():
    UserModel = get_user_model()
    try:
    	  users=UserModel.objects.all()
    	  events=Event.objects.all()
    	  now=datetime.now()
    	  for event in events:
    	      print(event.title)
    	      st=event.date_start
    	      ''' Check all The events and find those events which will be happen in next 2 to 3 hours than send the email to the user '''
    	      if now.year == st.year and now.month == st.month and now.day==st.day and st.hour+5-now.hour >= 2 and st.hour+5-now.hour <= 3:
    	          for user in users:
    	              send_mail("Reminder fo Event",event.title,'rameshsutliya@gamil.com',[user.email],fail_silently=False,)
    	          
    except UserModel.DoesNotExist:
        logging.warning("Tried to send email to non Existing User '%s' " % user_id)
