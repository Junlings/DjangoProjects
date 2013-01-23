from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('product_availbility.views',
    # Examples:
    url(r'^$', 'search', name='search'),
    url(r'^search.*/$', 'search_inventory', name='search_inventory'),
    
    
    
    )