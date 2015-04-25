from django.contrib import admin

from db.base.models import Satellite, Transponder, Suggestion


@admin.register(Satellite)
class SatelliteAdmin(admin.ModelAdmin):
    list_display = ('name', 'norad_cat_id')


@admin.register(Transponder)
class TransponderAdmin(admin.ModelAdmin):
    list_display = ('description', 'satellite', 'uplink_low',
                    'uplink_high', 'downlink_low', 'downlink_high')
    search_fields = ('satellite', )
    list_filter = ('mode', 'invert')


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('description', 'suggestion', 'user', 'satellite', 'uplink_low',
                    'uplink_high', 'downlink_low', 'downlink_high', 'approved')
    search_fields = ('satellite', 'approved')
    list_filter = ('mode', 'invert')

    def get_queryset(self, request):
        return Transponder.objects_all.filter(approved=False)
