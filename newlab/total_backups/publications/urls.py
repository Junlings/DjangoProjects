from django.conf.urls.defaults import patterns, include, url

from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _

from views import *

urlpatterns = patterns('publications.views',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^index/journal/$', 'journal_list',name='journal_list'),
    url(r'^index/$', 'publication_index',name='publication_index'),
    url(r'^lb/(?P<label>\w+)/$', 'publication_lb_index',name='publication_lb_index'),
    #url(r'^standard/lb/(?P<label>\w+)/$', 'standard_by_label',name='standard_by_label'),
    #url(r'^thesis/lb/(?P<label>\w+)/$', 'thesis_by_label',name='thesis_by_label'),
    #url(r'^book/lb/(?P<label>\w+)/$', 'book_by_label',name='book_by_label'),
    #url(r'^journal/lb/(?P<label>\w+)/$', 'journal_by_label',name='journal_by_label'),
    #url(r'^conference/lb/(?P<label>\w+)/$', 'conference_by_label',name='conference_by_label'),
)
