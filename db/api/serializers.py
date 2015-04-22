from rest_framework import serializers

from db.base.models import Satellite, Transponder


class SatelliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Satellite


class TransponderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transponder
