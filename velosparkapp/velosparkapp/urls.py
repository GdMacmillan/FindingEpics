from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout_then_login

from . import views

urlpatterns = (
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allaccess.urls')),
    url(r'^logout/$', logout_then_login, name='logout'),
    url(r'^contact/$', views.ContactView.as_view(), name='contact'),
    url(r'^(?P<pk>[0-9]+)/profile/$', views.ProfileView.as_view(), name='profile'),
)
