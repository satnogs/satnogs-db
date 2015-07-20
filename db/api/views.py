from rest_framework import viewsets

from db.api import serializers, filters
from db.base.models import Satellite, Transponder


class SatelliteView(viewsets.ModelViewSet):
    queryset = Satellite.objects.all()
    serializer_class = serializers.SatelliteSerializer
    lookup_field = 'norad_cat_id'


class TransponderView(viewsets.ModelViewSet):
    queryset = Transponder.objects.all()
    serializer_class = serializers.TransponderSerializer
    filter_class = filters.TransponderViewFilter
    lookup_field = 'uuid'
