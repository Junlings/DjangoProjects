#from django.conf.urls.defaults import *
from django.conf.urls.defaults import patterns, url
from djangoextension.djangorestframework.views import ListOrCreateModelView, InstanceModelView, ModelView, ListModelView, ListOrCreateModelUserView
from resources import AccountsResource, TransactionsResource

from views import *
from django.conf import settings
import django.contrib.auth.views


urlpatterns = patterns('djangoextension.financial.views',
    url(r'index/$', "financial_index", name='financial_index'),
    url(r'faccounts/create/$', "account_create_view", name='account_create'),
    url(r'faccounts/$', "account_list_view", name='account_list'),
    url(r'ftrans/$', "transaction_list_view", name='transaction_list'),
    url(r'ftrans/list/$', "Transaction_list_view2", name='transaction_list2'),
    url(r'ftrans/comission/$', "Transaction_list_comission", name='comission'),
    url(r'ftrans/transfer/$', "Transaction_list_transfer", name='internal_transfer'),
    url(r'ftrans/list/search/$', "Transaction_list_view_search", name='transaction_list_search'),
    url(r'faccount/list/$', "Account_list_view", name='transaction_list2'),
    url(r'faccount/list/search/$', "Account_list_view_search", name='transaction_list_search'),
    )

urlpatterns += patterns('',
    url(r'faccounts/api/$', ListOrCreateModelUserView.as_view(resource=AccountsResource), name='account-root'),
    url(r'faccounts/api/(?P<id>[^/]+)/$', InstanceModelView.as_view(resource=AccountsResource), name='account-post'),
    url(r'ftrans/api/$', ListModelView.as_view(resource=TransactionsResource), name='transaction-root'),
    url(r'ftrans/api/(?P<id>[^/]+)/$', InstanceModelView.as_view(resource=TransactionsResource), name='transaction-post'),
)

