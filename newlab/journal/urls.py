from django.conf.urls.defaults import patterns, include, url

from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _

from views import *

urlpatterns = patterns('journal.views',
    url(r'list/$', 'journal_list',name='journal_list'),
    url(r'detail/(?P<id>\d+)/$', 'journal_detail',name='journal_detail'),
)
