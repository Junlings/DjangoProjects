from django.conf.urls.defaults import patterns, include, url

from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _

from views import *

urlpatterns = patterns('conference.views',
    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^journal/list/$', 'journal_list',name='journal_list'),
    #url(r'^index/$', 'journal_index',name='journal_index'),
    #url(r'^paper/lb/(?P<label>\w+)/$', 'paper_by_label',name='paper_by_label'),
)
