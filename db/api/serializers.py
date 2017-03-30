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
    transmitter = serializers.SerializerMethodField()
    schema = serializers.SerializerMethodField()
    decoded = serializers.SerializerMethodField()
    frame = serializers.SerializerMethodField()

    class Meta:
        model = DemodData
        fields = ('norad_cat_id', 'transmitter', 'source', 'schema', 'decoded', 'frame',
                  'observer', 'timestamp')

    def get_norad_cat_id(self, obj):
        return obj.satellite.norad_cat_id

    def get_transmitter(self, obj):
        try:
            return obj.transmitter.uuid
        except:
            return ''

    def get_schema(self, obj):
        try:
            return obj.payload_telemetry.schema
        except:
            return ''

    def get_decoded(self, obj):
        return obj.payload_decoded

    def get_frame(self, obj):
        return obj.display_frame()


class SidsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemodData
        fields = ('satellite', 'payload_frame', 'station', 'lat', 'lng', 'timestamp')
