#from django.conf.urls.defaults import *
from django.conf.urls.defaults import patterns, url
from djangoextension.djangorestframework.views import ListOrCreateModelView, InstanceModelView, ModelView, ListModelView, ListOrCreateModelUserView
from resources import ItemProductResource

from views import *
from django.conf import settings
import django.contrib.auth.views


urlpatterns = patterns('manufacture.views',
    url(r'products/create/$', "Product_create_view", name='product_create'),
    url(r'manufacturers/create/$', "Manufacturer_create_view", name='Manufacturer_create'),
    url(r'products/create/batch$', "Product_create_batch_view", name='product_create_batch'),
    url(r'products/$', "Product_list_view", name='product_list'),
    url(r'products/null/$', ListOrCreateModelView.as_view(resource=ItemProductResource), name='product_list2'),
    )

urlpatterns += patterns('',
    url(r'products/api/$', ListOrCreateModelView.as_view(resource=ItemProductResource), name='product-root'),
    url(r'products/api/(?P<id>[^/]+)/$', InstanceModelView.as_view(resource=ItemProductResource), name='product-post'),

)

