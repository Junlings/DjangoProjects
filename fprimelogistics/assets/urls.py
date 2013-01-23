#from django.conf.urls.defaults import *
from django.conf.urls.defaults import patterns, url
#from djangoextension.djangorestframework.views import ListOrCreateModelView, InstanceModelView, ModelView, ListModelView, ListOrCreateModelUserView
#from resources import AssetResource

from views import *
from django.conf import settings
import django.contrib.auth.views


urlpatterns = patterns('assets.views',
    url(r'index/$', "Asset_index", name='asset_index'),
    #url(r'create/$', "Asset_create_view", name='asset_create'),
    url(r'list/$', "Asset_list_view", name='asset_list'),
    url(r'list/user/$', "Asset_list_user_view", name='asset_list_user'),
    url(r'list/search/$', "Asset_list_view_search", name='asset_list_search'),
    url(r'details/(?P<FSIN>[^/]+)/$', "Asset_details", name='asset_details'),
    #url(r'asset/null/$', ListOrCreateModelView.as_view(resource=AssetResource), name='asset_list2'),
    )

#urlpatterns += patterns('',
#    url(r'asset/api/$', ListOrCreateModelView.as_view(resource=AssetResource), name='asset-root'),
#    url(r'asset/api/(?P<id>[^/]+)/$', InstanceModelView.as_view(resource=AssetResource ), name='asset-post'),

#)

