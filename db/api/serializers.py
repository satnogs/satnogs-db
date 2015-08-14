from rest_framework import serializers

from db.base.models import Mode, Satellite, Transmitter


class ModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mode
        fields = ('id', 'name')


class SatelliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Satellite
        fields = ('norad_cat_id', 'name', 'names', 'image')


class TransmitterSerializer(serializers.ModelSerializer):
    norad_cat_id = serializers.SerializerMethodField()
    mode_id = serializers.SerializerMethodField()

    class Meta:
        model = Transmitter
        fields = ('uuid', 'description', 'alive', 'uplink_low', 'uplink_high',
                  'downlink_low', 'downlink_high', 'mode_id', 'invert',
                  'baud', 'norad_cat_id')

    def get_mode_id(self, obj):
        try:
            return obj.mode.id
	except:
	    return None

    def get_norad_cat_id(self, obj):
        return obj.satellite.norad_cat_id
