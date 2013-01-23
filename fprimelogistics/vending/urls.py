from django.conf.urls.defaults import patterns, include, url
#from django.views.generic.create_update import create_object, update_object

from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _

from views import *
from forms import *
from uti.encoder import JSONEncoder

urlpatterns = patterns('vending.views',
    # Examples:
    # url(r'^$', 'inventory.views.home', name='home'),
    #url(r'^products/', include('products.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^index/$', 'purchase_index',name='vending_index'),
    url(r'^create/$', 'purchase_create',name='vending_create'),
    url(r'^create/addfile/$', 'purchase_create_addfile',name='purchase_add_file'),
    url(r'^create/ajax/$', 'purchase_create_ajax',name='vending_create_ajax'),
    url(r'^list/$', 'purchase_list',name='vending_list'),
    url(r'^list/monthly/$', 'purchase_list_monthly',name='vending_list_monthly'),
    url(r'^list/search/$', 'purchase_search',name='vending_search'),
    #url(r'^purchases/create/success/$', 'purchase_create_success',name='success'),
    #url(r'^purchases/create/process/$', 'purchase_create_process',name='process'),
    #url(r'^purchases/create/fail/$', 'purchase_create_fail',name='fail'),
    #url(r'^purchases/create/$', 'create_purchase'),#, {'form_class':ItemTemplateForm,
                                                   #'template_name':'itemtemplate_form.html',
                                                   #'extra_context':{'object_name':_(u'item template')}},'template_create'),

)
