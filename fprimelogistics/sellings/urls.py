from django.conf.urls.defaults import patterns, include, url
#from django.views.generic.create_update import create_object, update_object

from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _

from views import *
from forms import *
from uti.encoder import JSONEncoder

urlpatterns = patterns('sellings.views',
    # Examples:
    # url(r'^$', 'inventory.views.home', name='home'),
    #url(r'^products/', include('products.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^create/$', 'purchase_create',name='vending_create'),
    #url(r'^create/addfile/$', 'purchase_create_addfile',name='purchase_add_file'),
    #url(r'^create/ajax/$', 'purchase_create_ajax',name='vending_create_ajax'),
    url(r'^list/$', 'sell_list',name='sell_list'),
    url(r'^index/$', 'sell_index',name='sell_index'),
    url(r'^list/monthly/$', 'sell_search_monthly',name='sell_search_monthly'),
    url(r'^list/search/$', 'sell_search',name='sell_search'),
    #url(r'^purchases/create/success/$', 'purchase_create_success',name='success'),
    #url(r'^purchases/create/process/$', 'purchase_create_process',name='process'),
    #url(r'^purchases/create/fail/$', 'purchase_create_fail',name='fail'),
    #url(r'^purchases/create/$', 'create_purchase'),#, {'form_class':ItemTemplateForm,
                                                   #'template_name':'itemtemplate_form.html',
                                                   #'extra_context':{'object_name':_(u'item template')}},'template_create'),

)
