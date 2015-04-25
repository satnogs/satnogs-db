from django.conf.urls import patterns, url, include
from rest_framework import routers

from db.api import views


router = routers.DefaultRouter()

router.register(r'transponders', views.TransponderView)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls))
)
