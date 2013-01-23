from django.conf.urls.defaults import patterns, include, url

from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _

from views import *

urlpatterns = patterns('contributor.views',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'(?P<id>\d+)/$', 'author_details',name='author_details'),

)
