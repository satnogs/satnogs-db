from rest_framework import viewsets, mixins, status
from rest_framework.parsers import FormParser, FileUploadParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.core.files.base import ContentFile

from db.api import serializers, filters, pagination
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


class TelemetryView(viewsets.ModelViewSet, mixins.CreateModelMixin):
    queryset = DemodData.objects.all()
    serializer_class = serializers.TelemetrySerializer
    filter_class = filters.TelemetryViewFilter
    permission_classes = (AllowAny, )
    parser_classes = (FormParser, FileUploadParser)
    pagination_class = pagination.LinkedHeaderPageNumberPagination

    def create(self, request, *args, **kwargs):
        data = {}

        data['satellite'] = Satellite.objects.get(norad_cat_id=request.data.get('noradID')).id
        data['station'] = request.data.get('source')
        timestamp = request.data.get('timestamp')
        data['timestamp'] = timestamp

        # Convert coordinates to omit N-S and W-E designators
        lat = request.data.get('latitude')
        lng = request.data.get('longitude')
        if any(x.isalpha() for x in lat):
            data['lat'] = (-float(lat[:-1]) if ('W' in lat) else float(lat[:-1]))
        else:
            data['lat'] = float(lat)
        if any(x.isalpha() for x in lng):
            data['lng'] = (-float(lng[:-1]) if ('S' in lng) else float(lng[:-1]))
        else:
            data['lng'] = float(lng)

        # Create file out of frame string
        frame = ContentFile(request.data.get('frame'), name='sids')
        data['payload_frame'] = frame

        serializer = serializers.SidsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)
