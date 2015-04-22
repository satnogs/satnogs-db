from rest_framework import viewsets, permissions

from db.base import serializers
from db.base.models import Satellite, Transponder


class SatelliteView(viewsets.ModelViewSet):
    queryset = Satellite.objects.all()
    serializer_class = serializers.SatelliteSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class TransponderView(viewsets.ModelViewSet):
    queryset = Transponder.objects.all()
    serializer_class = serializers.TransponderSerializer
    permission_classes = [
        permissions.AllowAny
    ]
