import django_filters

from db.base.models import Transmitter, DemodData


class TransmitterViewFilter(django_filters.FilterSet):
    class Meta:
        model = Transmitter
        fields = ['mode', 'satellite__norad_cat_id']


class TelemetryViewFilter(django_filters.FilterSet):
    satellite = django_filters.NumberFilter(name='satellite__norad_cat_id',
                                            lookup_expr='exact')

    class Meta:
        model = DemodData
        fields = ['satellite']
