#from django.conf.urls.defaults import *
from django.conf.urls.defaults import patterns, url
from djangorestframework.views import ListOrCreateModelView, InstanceModelView, ModelView, ListModelView
from contacts.resources import TestResource, AddressResource

from views import *
from django.conf import settings
import django.contrib.auth.views


urlpatterns = patterns('djangoextension.contacts.views',
    url(r'address/create/$', "root_view", name='root'),
    url(r'address/$', "list_view", name='list'),
    #url(r'address/query/(?P<query>[^/]+/$)', "query_view", name='query'),
    #url(r'address/.*$)', "query_view", name='query'),
    )

urlpatterns += patterns('',
    url(r'test/$', ListOrCreateModelView.as_view(resource=TestResource), name='test-root'),
    url(r'test/(?P<id>[^/]+)/$', InstanceModelView.as_view(resource=TestResource), name='test-post'),
    url(r'address/api/$', ListModelView.as_view(resource=AddressResource), name='address-root'),
    url(r'address/api/(?P<id>[^/]+)/$', InstanceModelView.as_view(resource=AddressResource), name='address-post'),

)

