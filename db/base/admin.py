from django.contrib import admin
from django.core.urlresolvers import reverse

from db.base.models import Satellite, Transponder, Suggestion


@admin.register(Satellite)
class SatelliteAdmin(admin.ModelAdmin):
    list_display = ('name', 'norad_cat_id')


@admin.register(Transponder)
class TransponderAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'description', 'satellite', 'uplink_low',
                    'uplink_high', 'downlink_low', 'downlink_high',)
    search_fields = ('satellite', 'uuid',)
    list_filter = ('mode', 'invert')
    readonly_fields = ('uuid', 'satellite', 'approved',)


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'description', 'transponder_uuid', 'user', 'satellite', 'uplink_low',
                    'uplink_high', 'downlink_low', 'downlink_high',)
    search_fields = ('satellite', 'uuid',)
    list_filter = ('mode', 'invert')
    readonly_fields = ('uuid', 'satellite', 'transponder', 'approved', 'user',
                       'citation', 'transponder_data')

    def transponder_uuid(self, obj):
        try:
            return obj.transponder.uuid
        except:
            return '-'

    def transponder_data(self, obj):
        if obj.transponder:
            redirect_url = reverse('admin:base_transponder_changelist')
            extra = '{0}'.format(obj.transponder.pk)
            return '<a href="{}">Trnasponder Initial Data</a>'.format(
                redirect_url + extra)
        else:
            return '-'
    transponder_data.allow_tags = True
