from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from event.models import Event,Guest,MediaLinks,UploadMedai
from django.views.generic import TemplateView,ListView,DetailView
from django.db.models import Q

class HomeView(TemplateView):
	template_name = 'basic/home.html'
	def get(self,request):
		event=Event.objects.all().order_by('-date_start')[:20]
		guest=Guest.objects.all().order_by('-name')[:5]
		args={'event':event,'guest':guest}
		return render(request,self.template_name,args)



class EventListView(ListView):
	model=Event
	template_name='event/event_list.html'
	context_object_name='KiiT Event'
	paginate_by=5
	queryset=Event.objects.all().order_by('-date_start','date_end')
'''	def get_queryset(self,request):
		queryset = super(EventListView, self).get_queryset(request)
		queryset = queryset.objects.all().
		return queryset
'''		
class UpComingEvents(ListView):
	model=Event
	template_name = 'event/upcomingevents.html'
	paginate_by = 6
	queryset = Event.objects.all().order_by('date')
	

class PastEvents(ListView):
	model = Event
	template_name = 'event/pastevents.html'
	paginate_by = 10
	queryset = Event.objects.all().order_by('-date')

class GuestList(ListView):
	model = Guest
	template_name = 'event/guestlist.html'
	paginate_by = 8
	queryset = Guest.objects.all().order_by('name')
	

class MediaList(ListView):
	model = UploadMedai
	template_name = 'event/medialist.html'
	paginate_by = 10
	queryset = Guest.objects.all().order_by('eventname')

class EventDetails(DetailView):
	model=Event
	template_name='event/event.html'
	def get_context_data(self,**kwargs):
		context = super(DetailView, self).get_context_data(**kwargs)
		obj = self.get_object()
		obj.view_count = obj.view_count + 1
		obj.save()
		return context


from django.http import JsonResponse
def autocomplete(request):
	if request.is_ajax():
		queryset = Event.objects.filter(title__startswith=request.GET.get('search', None))
		list = []
		for i in queryset:
				list.append(i.title)
		data = {
				'list': list,
		}
		return JsonResponse(data)

def searchresult(request):
	if request.method == 'GET':
		eventname =  request.GET.getlist('search')
		try:
			status = Event.objects.filter(title__icontains=eventname)
			#Add_prod class contains a column called 'bookname'
		except Add_prod.DoesNotExist:
			status = None
		return render(request,"event/search.html",{"title":status})
	else:
		return render(request,"event/search.html",{})
