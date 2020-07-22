from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.template import Template, Context
from django.http import HttpResponse
from django.conf import settings

#Only Here I am Getting Error:Import Error
#from core.models import #ScheduledReport, ScheduledReportGroup, ReportRecipient
#from core.models import ReportRecipient
class ScheduledReportConfig(object):
    def __init__(self, scheduled_report):
        """
            Expects a scheduled report object and inititializes
            its own scheduled_report attribute with it
        """
        self.scheduled_report = scheduled_report
    def get_report_config(self):
        """
            Returns the configuration related to a scheduled report, needed
            to populate the email
        """
        return {
                "template_context": self._get_related_reports_data(),
                "recipients": self._get_report_recipients()
                }
    def _get_related_reports_data(self):
        """
            Returns the list of reports data which needs to be sent out in a scheduled report
        """
#        //Logic to get the reports data and format it as you need
        pass
    def _get_report_recipients(self):
        """
            Returns the recipient list for a scheduled report
        """
#        //Logic to get the recipients for a scheduled report
        pass
def create_email_data(content=None):
#    //Generate html for the the email body
    content = '''
            Testing for fully functional website

         ''' + str(content) + ''''''
    return content
def send_emails():
        current_time = datetime.now()
#        //Get all the reports which have to sent out till the current time.
        scheduled_reports = ScheduledReport.objects.filter(next_run_at__lt = current_time)
        for scheduled_report in scheduled_reports:
            report_config = ScheduledReportConfig(scheduled_report).get_report_config()
#            //Specify the template path you want to send out in the email.
            template = Template(create_email_data('path/to/your/email_template.html'))
#            //Create your email html using Django's context processor
            report_template = template.render(Context(report_config['template_context']))
            scheduled_report.save()
            if not scheduled_report.subject:
                pass
#                //Handle exception for subject not provided
            if not report_config['recipients']:
                pass
#                //Handle exception for recipients not provided
            send_mail(
                scheduled_report.subject, 'Fully Functional.',
                settings.EMAIL_HOST_USER, report_config['<email>'],
                fail_silently=False, html_message=report_template
            )
