from django.conf.urls.defaults import patterns, include, url

from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _

from views import *

urlpatterns = patterns('publications.views',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'journal/$', 'journal_paper_list',name='journal_paper_list'),
    url(r'conference/$', 'conference_paper_list',name='conference_paper_list'),
    url(r'report/$', 'report_paper_list',name='report_paper_list'),
    url(r'thesis/$', 'thesis_paper_list',name='thesis_paper_list'),
    url(r'books/$', 'books_paper_list',name='books_paper_list'),
    url(r'standards/$', 'stands_paper_list',name='stands_paper_list'),
    
    url(r'index/$', 'publication_index',name='publication_index'),
    url(r'lb/(?P<label>\w+)/$', 'publication_lb_index',name='publication_lb_index'),
    url(r'keywords/(?P<id>\d+)/$', 'publication_keyword_detail',name='publication_keyword_detail'),
    
    
    url(r'journal/add/$', 'publication_create',name='publication_create'),
)
