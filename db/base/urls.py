from django.conf.urls import url

from db.base import views


base_urlpatterns = ([
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^satellite/(?P<norad>[0-9]+)/$', views.satellite, name='satellite'),
    url(r'^frames/(?P<norad>[0-9]+)/$', views.request_export,
        name='request_export_all'),
    url(r'^frames/(?P<norad>[0-9]+)/(?P<period>[0-9]+)/$', views.request_export,
        name='request_export'),
    url(r'^satellite_position/(?P<sat_id>[0-9]+)/$', views.satellite_position,
        name='satellite_position'),
    url(r'^suggestion/$', views.suggestion, name='suggestion'),
    url(r'^statistics/$', views.statistics, name='statistics'),
    url(r'^stats/$', views.stats, name='stats'),
    url(r'^users/edit/$', views.users_edit, name='users_edit'),
    url(r'^robots\.txt$', views.robots, name='robots'),
])
