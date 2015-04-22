from django.contrib import admin

from db.base.models import Satellite, Transponder


class SatelliteAdmin(admin.ModelAdmin):
    list_display = ('name', 'norad_cat_id')


class TransponderAdmin(admin.ModelAdmin):
    list_display = ('description', 'satellite', 'uplink_low',
                    'uplink_high', 'downlink_low', 'downlink_high')
    search_fields = ('satellite', )
    list_filter = ('mode', 'invert', 'approved')


admin.site.register(Satellite, SatelliteAdmin)
admin.site.register(Transponder, TransponderAdmin)
