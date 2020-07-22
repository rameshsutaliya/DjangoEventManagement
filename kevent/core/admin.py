from django.contrib import admin
admin.site.site_header = 'Admin @ Ramesh Sutaliya'
# Register your models here.
from core.models import User
@admin.register(User)
#@admin.site.site_header("Yeah!! I am Admin")#proxy error
#admin.site.site_header = 'Yeah!! I am Admin'

class UserAdmin(admin.ModelAdmin):
	pass
	
#from django.contrib import admin
from django.template.defaultfilters import escape
#from django.core.urlresolvers import reverse
from django.urls import reverse
from core.models import ScheduledReport, ReportRecipient, ScheduledReportGroup,Report
from core.forms import ScheduledReportForm
#@admin.register(Report)
#class ReportAdmin(admin.TabularInline):
#    model=Report

class ReportRecipientAdmin(admin.TabularInline):
    model = ReportRecipient
class ScheduledReportAdmin(admin.ModelAdmin):
    """
        List display for Scheduled reports in Django admin
    """
    model = ScheduledReport
    list_display = ('id', 'get_recipients')
    inlines = [
        ReportRecipientAdmin
    ]
    form = ScheduledReportForm
    def get_recipients(self, model):
        recipients = model.reportrecep.all().values_list('email', flat=True)
        if not recipients:
            return 'No recipients added'
        recipient_list = ''
        for recipient in recipients:
            recipient_list = recipient_list + recipient + ', '
        return recipient_list[:-2]
    get_recipients.short_description = 'Recipients'
    get_recipients.allow_tags = True
class ScheduledReportGroupAdmin(admin.ModelAdmin):
    """
        List display for ScheduledReportGroup Admin
    """
    model = ScheduledReportGroup
    list_display = ('get_scheduled_report_name','get_report_name')
    def get_scheduled_report_name(self, model):
        return model.scheduled_report.subject
    def get_report_name(self, model):
        return model.report.name
    get_scheduled_report_name.short_description = "Scheduled Report Name"
    get_report_name.short_description = "Report Name"
    show_change_link = True
    get_report_name.allow_tags = True
admin.site.register(ScheduledReport, ScheduledReportAdmin)
admin.site.register(ScheduledReportGroup, ScheduledReportGroupAdmin)
