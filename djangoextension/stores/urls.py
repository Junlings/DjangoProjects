from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('stores.views',
    # Examples:
    url(r'^map/$', 'store_map', name='store_map'),
    url(r'^map/search/.*$', 'store_map_search', name='store_map_search'),
    url(r'^staples/(?P<store_id>\d+)/$', 'get_local_staples', name='get_local_staples'),
    url(r'^staples/state/$', 'get_local_staples_state', name='get_local_staples_state'),
    url(r'^staples/storelist/$', 'ajax_storelist', name='ajax_storelist'),
    url(r'^staples/test/$', 'test_storelist', name='test_storelist'),
    )