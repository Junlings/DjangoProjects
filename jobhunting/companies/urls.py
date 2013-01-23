from django.conf.urls.defaults import *

urlpatterns = patterns('companies.views',
    url(r'^list$', 'company_list', (), 'company_list'),
    #url(r'^detail/(?P<object_id>\d+)/$', 'company_detail', (), 'company_detail'),
)
