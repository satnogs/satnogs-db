import django_filters

from db.base.models import Transponder


class TransponderViewFilter(django_filters.FilterSet):
    class Meta:
        model = Transponder
        fields = ['mode', 'satellite__norad_cat_id']
