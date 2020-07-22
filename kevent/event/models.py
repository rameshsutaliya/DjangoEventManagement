from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse # for reverse the url pattern
from django.core.validators import FileExtensionValidator #for validate the file type
#from django.db.models.signals import post_delete
#from django.dispatch import receiver #for deleting the file from the system.
# First of all we needs to store the Guest
# Guest Table stores little bit information about the Guest of the event.
def event_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'images/event/'.format(instance.title, filename)

class Event(models.Model):
	title = models.CharField('Title*',max_length=300,help_text='Enter the Event Title or Heading of the event')
	event_poster = models.ImageField(upload_to=event_directory_path,help_text="Please Upload the Event poster at here..")
	#Make The Guest as many to many...
#	guest = models.ManyToManyField("Guest",Guest,blank=True,null=True,help_text='Either Select a Visited Guest or Add if Guest not visited')
	body = models.TextField("Event Information *",null=True,help_text='Other Detail or message of the Event',)
	date_start = models.DateTimeField("Start*",null=True,help_text='When will be start the event?',)
	date_end=models.DateTimeField("End ",null=True,blank=True,help_text='When will be event end??',)
	event_cate = models.CharField("Event Categories:",max_length=200,default="KIIT",null=True,help_text="In which Category this event belongs ?")
	
	event_web = models.URLField("Event Website :",null=True,blank=True,help_text="If Event has a website then put that web link at here!.",)	
	event_addr1 = models.CharField("Event address Line 1*:",max_length=150,default="KIIT deemed to be University",null=True,help_text="Where this event will happen?",)
	event_addr2 = models.CharField("Event address Line 2",max_length=100,default="KIIT",null=True,blank=True)
	event_addr3 = models.CharField("State :",max_length=100,default="Odisha",null=True,blank=True,help_text="State where this event will be happen")
	event_addr4 = models.CharField("Country* : ",max_length=100,default="India",null=True,help_text="If the event going to outside to the country please mention here...Keep Smile..")
	zipcode = models.CharField("Zip Code*:",max_length=8,null=True,default="751024",help_text="Please Provide the postel code..")
	view_count = models.PositiveIntegerField("View Count", default=1)
	class Meta:
		indexes = [models.Index(fields=['title'])]
		ordering = ['-id']
	def __str__(self):
		if self.title:
			return self.title
			#return '"%s" Chief Guest Mr. %s' % (self.title,self.guest)
	
	def get_absolute_url(self):
		"""Returns the url to access a detail record for this event."""
		return reverse('guest-detail', args=[str(self.id)])

    
class Guest(models.Model):
	name = models.CharField(max_length=150,null=True,help_text='Who is the guest in the event??')
	eventname=models.ForeignKey(Event,on_delete=models.CASCADE)
	organization = models.CharField(max_length=200,null=True,help_text='From which Organization this guest belongs ?')
	profile = models.CharField(max_length=200,blank=True,help_text='What is profile of the Guest in the Organization?')
	addressLine1 = models.CharField(max_length=100,null=True,blank=True,help_text="I don't think that you needs any help here!")
	addressLine2 = models.CharField(max_length=100,null=True,blank=True)
	zipCode = models.CharField(max_length=10,null=True,blank=True,help_text="In other words,Do you know the pincode ?")
	state=models.CharField(max_length=50,null=True,blank=True)
	country=models.CharField(max_length=150,null=True,blank=True)
	contact=models.CharField(max_length=14,null=True,blank=True,help_text='Contact number if available')
	email = models.EmailField(max_length=70,blank=True,help_text="Enter the guest's email")
	
	class Meta:
		ordering = ['name']
	
	def __str__(self):
		"""String for representing the Model object."""
		if self.name:
			return self.name
	def get_absolute_url(self):
		"""Returns the url to access a detail record for this guest."""
		return reverse('guest-detail', args=[str(self.id)])

# Second We needs to store the Event information.
# this is our event table.

class MediaLinks(models.Model):
	MEDIA_TYPE=(('i','Image'),('v','Vedio'),('d',"Document"),('a','Audio'),)
	eventname = models.ForeignKey(Event,on_delete=models.CASCADE)
	mediaType=models.CharField(max_length=1,choices=MEDIA_TYPE,null=True,blank=True,help_text="Choose the type of Media",)
	hyperlink = models.URLField(null=True,blank=True,help_text="paste the media's url here.")
	def __str__(self):
		if self.eventname:
			return '%s \n Link:%s' % (self.eventname,self.hyperlink)
		else:
			return self.eventname

# After Creating the Event we needs to store the Media files of the event.
# This is the media table which store's information about the media files.

class UploadMedai(models.Model):
	MEDIA_TYPE=(('i','Image'),('v','Vedio'),('p',"Pdf"),)
	eventname = models.ForeignKey(Event,on_delete=models.CASCADE)
	uploaded_at = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to='images/',null=True,blank=True)
	pdf = models.FileField(upload_to='pdfs/',validators=[FileExtensionValidator(allowed_extensions=['pdf'])],null=True,blank=True)
	video = models.FileField(upload_to='videos/',validators=[FileExtensionValidator(allowed_extensions=['mp4','mov','3gp','ogg','oga','ogv','ogx','wmv','wma','webm','flv'])],null=True,blank=True)
	somethingSpecific = models.CharField(max_length=255, blank=True,null=True)
	class Meta:
		indexes = [models.Index(fields=['eventname'])]
		ordering = ['-uploaded_at']
	def __str__(self):
		if self.somethingSpecific:
			return self.somethingSpecific
		else:
			return self.eventname
	def get_absolute_url(self):
		"""Returns the url to access a detail record for this guest."""
		return reverse('medai-detail', args=[str(self.id)])
'''
@receiver(post_delete, sender=UploadMedai)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)
    instance.video.delete(False)
    instance.pdf.delete(False)
'''
# Create a Event Categories
#from core.tasks import trigger_emails
#It is an assosiation ..
def create_media(sender,**kwargs):
	if kwargs['created']:
#		uploadmedia=UploadMedai.objects.create(eventname=kwargs['instance'])
		linkmedia=MediaLinks.objects.create(eventname=kwargs['instance'])
		
post_save.connect(create_media,sender=Event)
'''
@receiver(post_delete, sender=Event)
def submission_delete(sender, instance, **kwargs):
    instance.event_poster.delete(False)
'''
