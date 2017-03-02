from rest_framework import serializers

from db.base.models import Mode, Satellite, Transmitter, DemodData


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


class TelemetrySerializer(serializers.ModelSerializer):
    norad_cat_id = serializers.SerializerMethodField()
    appendix = serializers.SerializerMethodField()
    telemetry = serializers.SerializerMethodField()

    class Meta:
        model = DemodData
        fields = ('norad_cat_id', 'appendix', 'telemetry')

    def get_norad_cat_id(self, obj):
        return obj.satellite.norad_cat_id

    def get_appendix(self, obj):
        try:
            return obj.payload_telemetry.schema
        except:
            return ''

    def get_telemetry(self, obj):
        return obj.payload_decoded


class SidsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemodData
        fields = ('satellite', 'payload_frame', 'station', 'lat', 'lng', 'timestamp')
