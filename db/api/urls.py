from rest_framework import routers

from db.api import views


router = routers.DefaultRouter()

router.register(r'modes', views.ModeView)
router.register(r'satellites', views.SatelliteView)
router.register(r'transmitters', views.TransmitterView)
router.register(r'telemetry', views.TelemetryView)

api_urlpatterns = router.urls
