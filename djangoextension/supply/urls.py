#from django.conf.urls.defaults import *
from django.conf.urls.defaults import patterns, url
from djangoextension.djangorestframework.views import ListOrCreateModelView, InstanceModelView, ModelView, ListModelView, ListOrCreateModelUserView
from resources import ItemTemplateResource

from views import *
from django.conf import settings
import django.contrib.auth.views


urlpatterns = patterns('supply.views',
    url(r'supplies/create/$', "Supplies_create_view", name='supplies_create'),
    url(r'items/create/$', "items_create_view", name='items_create'),
    url(r'supplies/create/batch$', "Supplies_create_batch_view", name='supplies_create_batch'),
    url(r'supplies/create/search.*/$', "Supplies_create_search_view", name='supplies_create_search'),
    url(r'supplies/create/post/$', "Supplies_create_search_view_post", name='supplies_create_search_post'),
    url(r'add/$', "Supplies_add_view", name='supplies_add_view'),
    url(r'add/local.*/$', "Supplies_add_view_local", name='supplies_add_view_local'),
    url(r'add/search.*/$', "Supplies_add_view_search", name='supplies_add_view_search'),
    url(r'index/$', "Supplies_index_view", name='supplies_index'),
    )

urlpatterns += patterns('',
    url(r'supplies/api/$', ListOrCreateModelView.as_view(resource=ItemTemplateResource), name='product-root'),
    url(r'supplies/api/(?P<id>[^/]+)/$', InstanceModelView.as_view(resource=ItemTemplateResource), name='product-post'),

)

