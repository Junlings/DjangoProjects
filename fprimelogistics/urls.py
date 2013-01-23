from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.conf import settings

urlpatterns = patterns('',
    # Examples:

    url(r'^$',include('main.urls')),
    url(r'^contacts/',include('djangoextension.contacts.urls')),
    url(r'^financial/',include('djangoextension.financial.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^manufacture/',include('manufacture.urls')),
    url(r'^supply/',include('supply.urls')),
    url(r'^avail/',include('product_availbility.urls')),
    url(r'^assets/',include('assets.urls')),
    url(r'^purchases/',include('vending.urls')),
    url(r'^sells/',include('sellings.urls')),
    #url(r'^accounts/inventory/', include('accounts.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)



if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )