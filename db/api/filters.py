import django_filters

from db.base.models import Transmitter


class TransmitterViewFilter(django_filters.FilterSet):
    class Meta:
        model = Transmitter
        fields = ['mode', 'satellite__norad_cat_id']
