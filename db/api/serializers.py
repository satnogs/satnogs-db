from rest_framework import serializers

from db.base.models import Satellite, Transponder


class SatelliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Satellite


class TransponderSerializer(serializers.ModelSerializer):
    norad_cat_id = serializers.SerializerMethodField()

    class Meta:
        model = Transponder
        fields = ('uuid', 'description', 'alive', 'uplink_low', 'uplink_high',
                  'downlink_low', 'downlink_high', 'mode', 'invert',
                  'baud', 'norad_cat_id')

    def get_norad_cat_id(self, obj):
        return obj.satellite.norad_cat_id
