from rest_framework import viewsets

from db.api import serializers, filters
from db.base.models import Satellite, Transmitter


class SatelliteView(viewsets.ModelViewSet):
    queryset = Satellite.objects.all()
    serializer_class = serializers.SatelliteSerializer
    lookup_field = 'norad_cat_id'


class TransmitterView(viewsets.ModelViewSet):
    queryset = Transmitter.objects.all()
    serializer_class = serializers.TransmitterSerializer
    filter_class = filters.TransmitterViewFilter
    lookup_field = 'uuid'
