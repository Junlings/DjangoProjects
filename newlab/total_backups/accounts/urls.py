from django.conf.urls.defaults import *
from accounts.views import *
from django.conf import settings
import django.contrib.auth.views

urlpatterns = patterns('',
    (r'^login/$', 'django.contrib.auth.views.login',
     {'template_name': 'login.html'}),
    (r'profile/$',profile),
    (r'logout/$','django.contrib.auth.views.logout')
    )


