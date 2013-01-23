#from django.conf.urls.defaults import *
from django.conf.urls.defaults import patterns, url
#from djangoextension.djangorestframework.views import ListOrCreateModelView, InstanceModelView, ModelView, ListModelView, ListOrCreateModelUserView
#from resources import ItemTemplateResource

from views import *
from django.conf import settings
import django.contrib.auth.views


urlpatterns = patterns('feedscollect.views',
    url(r'collect/action/$', "Collect_feeds_action", name='collect_feeds_action'),
    url(r'collect/$', "Collect_feeds", name='collect_feeds'),
    )

