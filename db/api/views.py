from rest_framework import viewsets

from db.base import serializers
from db.base.models import Satellite, Transponder


class TransponderView(viewsets.ModelViewSet):
    queryset = Transponder.objects.all()
    serializer_class = serializers.TransponderSerializer
