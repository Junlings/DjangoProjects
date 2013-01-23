from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    url(r'^$','main.views.home'),
    url(r'^author/',include('contributor.urls')),
    url(r'^user/',include('main.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^journal/', include('journal.urls')),
    url(r'^publications/', include('publications.urls')),
    url(r'^lreviews/', include('lreviews_2.urls')),
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