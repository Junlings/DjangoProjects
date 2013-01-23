from django.conf.urls.defaults import patterns, include, url

from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _

from views import *

urlpatterns = patterns('lreviews_2.views',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^project/index/$', 'project_index',name='project_index'),
    url(r'^project/(?P<id>\d)/$', 'project_details',name='project_details'),
    url(r'^project/(?P<id>\d)/(?P<label>\w+)/$', 'project_lb_details',name='project_lb_details'),
    url(r'^project/submit/$', 'project_submit',name='project_submit'),
)
