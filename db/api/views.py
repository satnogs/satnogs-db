from rest_framework import viewsets

from db.api import serializers, filters
from db.base.models import Mode, Satellite, Transmitter, DemodData


class ModeView(viewsets.ReadOnlyModelViewSet):
    queryset = Mode.objects.all()
    serializer_class = serializers.ModeSerializer


class SatelliteView(viewsets.ReadOnlyModelViewSet):
    queryset = Satellite.objects.all()
    serializer_class = serializers.SatelliteSerializer
    lookup_field = 'norad_cat_id'


class TransmitterView(viewsets.ReadOnlyModelViewSet):
    queryset = Transmitter.objects.all()
    serializer_class = serializers.TransmitterSerializer
    filter_class = filters.TransmitterViewFilter
    lookup_field = 'uuid'


class TelemetryView(viewsets.ReadOnlyModelViewSet):
    queryset = DemodData.objects.all()
    serializer_class = serializers.TelemetrySerializer
    filter_class = filters.TelemetryViewFilter
