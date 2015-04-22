from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',

    # Base
    url(r'^$', include('db.base.urls')),

    # Accounts
    url(r'^accounts/', include('allauth.urls')),

    # API
    url(r'^api/', include('db.api.urls')),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
