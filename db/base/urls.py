from django.conf.urls import url

from db.base import views


base_urlpatterns = ([
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^satellite/(?P<norad>[0-9]+)/$', views.satellite, name='satellite'),
    url(r'^suggestion/$', views.suggestion, name='suggestion'),
    url(r'^statistics/$', views.statistics, name='statistics'),
    url(r'^robots\.txt$', views.robots, name='robots'),
])
