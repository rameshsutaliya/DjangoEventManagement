from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
 
class UserAccountManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email address must be provided')
 
        if not password:
            raise ValueError('Password must be provided')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)
 
    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True 
        return self._create_user(email, password, **extra_fields)
import uuid

class User(AbstractBaseUser, PermissionsMixin):
 
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    objects = UserAccountManager()
    email = models.EmailField('email', unique=True, blank=False, null=False)
    full_name = models.CharField('full name', blank=True, null=True, max_length=400)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    is_verified = models.BooleanField('verified', default=False) # Add the `is_verified` flag
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)
    def get_short_name(self):
        return self.email
    def get_full_name(self):
        return self.email
    def __unicode__(self):
        return self.email
from django.db.models import signals
#from django.core.mail import send_mail
#from django.urls import reverse 

'''def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_verified:
        # Send verification email
        send_mail(
            'Verify your kiitEvent account',
            'Follow this link to verify your account: '
                'http://127.0.0.1:8000%s' % reverse('verify', kwargs={'uuid': str(instance.verification_uuid)}),
            'rameshsutliya@gmail.com',
            [instance.email],
            fail_silently=False,
        )
 
signals.post_save.connect(user_post_save, sender=User)
'''

'''after celery engine.'''

from core.tasks import send_verification_email #,trigger_emails

def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_verified:
        # Send verification email
        send_verification_email.delay(instance.pk)
signals.post_save.connect(user_post_save, sender=User)

from datetime import datetime






class Report(models.Model):
    reportmessage=models.CharField(max_length=100)
    time=models.DateTimeField()



from croniter import croniter
class ScheduledReport(models.Model):
    """
		    Contains email subject and cron expression,to evaluate when the email has to be sent
    """
    subject = models.CharField(max_length=200)
    last_run_at = models.DateTimeField(null=True, blank=True)
    next_run_at = models.DateTimeField(null=True, blank=True)
    cron_expression = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        """
        function to evaluate "next_run_at" using the cron expression, so that it is updated once the report is sent.
        """
        self.last_run_at = datetime.now()
        iter = croniter(self.cron_expression, self.last_run_at)
        self.next_run_at = iter.get_next(datetime)
        super(ScheduledReport, self).save(*args, **kwargs)
    def __str__(self):
        return self.subject


class ScheduledReportGroup(models.Model):
    """
        Many to many mapping between reports which will be sent out in a
        scheduled report
    """
    report = models.ForeignKey(Report,on_delete=models.CASCADE,related_name='report')
    scheduled_report = models.ForeignKey(ScheduledReport,on_delete=models.CASCADE,related_name='relatedscheduledreport')


class ReportRecipient(models.Model):
    """
        Stores all the recipients of the given scheduled report
    """
    email = models.EmailField()
    scheduled_report = models.ForeignKey(ScheduledReport, on_delete=models.CASCADE,related_name='reportrecep')
