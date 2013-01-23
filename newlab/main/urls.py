from django.conf.urls.defaults import *

urlpatterns = patterns('main.views',
    url(r'^$', 'home', (), 'home'),
    url(r'reflib/(?P<id>\d)/$', 'reflib', (), 'reflib'),
)
