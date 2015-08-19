from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

handler404 = 'db.base.views.custom_404'
handler500 = 'db.base.views.custom_500'

urlpatterns = patterns(
    '',

    # Base
    url(r'^', include('db.base.urls')),

    # Accounts
    url(r'^accounts/', include('allauth.urls')),

    # API
    url(r'^api/', include('db.api.urls')),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^404/$', handler404),
        url(r'^500/$', handler500),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
