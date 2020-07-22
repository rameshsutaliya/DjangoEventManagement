from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView,ListView,DetailView
from event.models import Event,Guest
#from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from core.views import verify
from django.conf.urls.static import static
from django.conf import settings
from event.views import EventListView,HomeView,EventDetails,autocomplete,searchresult


urlpatterns = [
    path('admin/doc/',include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', HomeView.as_view(), name='home'),
    path('verify/<uuid>',verify,name='verify'),#This will verify the Email account.
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', login_required(auth_views.LogoutView.as_view(next_page=reverse_lazy('login'))), name='logout'),
    path('password_change/',auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'),name='password_change'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),name='password_change_done'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
    path('events/',login_required(EventListView.as_view()),name="events"),
    path('event/<int:pk>',login_required(EventDetails.as_view()),name="eventdet" ),
    path('guest/list',ListView.as_view(queryset=Guest.objects.all().order_by('-name'),template_name='event/guest_list.html'),name='guests'),
    path('guest/<int:pk>',DetailView.as_view(model=Guest,template_name='event/guest_det.html'),name="guestdet"),
    path('ajax/autocomplete/', autocomplete, name='ajax_autocomplete'),
    #upto here is perfact...
    path('q/',searchresult,name='search'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
