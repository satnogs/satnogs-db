from rest_framework import serializers

from db.base.models import Transponder


class TransponderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transponder
