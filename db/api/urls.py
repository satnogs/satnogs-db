from django.conf.urls import patterns, url, include
from rest_framework import routers

from db.api import views


router = routers.DefaultRouter()

router.register(r'modes', views.ModeView)
router.register(r'satellites', views.SatelliteView)
router.register(r'transmitters', views.TransmitterView)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls))
)
