import logging

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from db.base.models import Mode, Satellite, Transmitter, Suggestion, DemodData, Telemetry

logger = logging.getLogger('db')


@admin.register(Mode)
class ModeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Satellite)
class SatelliteAdmin(admin.ModelAdmin):
    list_display = ('name', 'norad_cat_id')


@admin.register(Transmitter)
class TransmitterAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'description', 'satellite', 'uplink_low',
                    'uplink_high', 'downlink_low', 'downlink_high')
    search_fields = ('satellite__id', 'uuid',)
    list_filter = ('mode', 'invert')
    readonly_fields = ('uuid', 'satellite', 'approved',)


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'description', 'transmitter_uuid', 'user', 'satellite', 'uplink_low',
                    'uplink_high', 'downlink_low', 'downlink_high',)
    search_fields = ('satellite', 'uuid',)
    list_filter = ('mode', 'invert')
    readonly_fields = ('uuid', 'satellite', 'transmitter', 'approved', 'user',
                       'citation', 'transmitter_data')
    actions = ['approve_suggestion']

    def approve_suggestion(self, request, queryset):
        for obj in queryset:
            try:
                transmitter = Transmitter.objects.get(id=obj.transmitter.id)
                transmitter.update_from_suggestion(obj)
                obj.delete()
            except (Transmitter.DoesNotExist, AttributeError):
                obj.approved = True
                obj.citation = ''
                obj.user = None
                obj.save()

            # Notify user
            current_site = get_current_site(request)
            subject = '[{0}] Your suggestion was approved'.format(current_site.name)
            template = 'emails/suggestion_approved.txt'
            data = {
                'satname': obj.satellite.name,
                'site_name': current_site.name
            }
            message = render_to_string(template, {'data': data})
            try:
                obj.user.email_user(subject, message, from_email=settings.DEFAULT_FROM_EMAIL)
            except:
                logger.error(
                    'Could not send email to user',
                    exc_info=True
                )

        rows_updated = queryset.count()

        # Print a message
        if rows_updated == 1:
            message_bit = '1 suggestion was'
        else:
            message_bit = '{0} suggestions were'.format(rows_updated)
        self.message_user(request, '{0} successfully approved.'.format(message_bit))

    approve_suggestion.short_description = 'Approve selected suggestions'

    def transmitter_uuid(self, obj):
        try:
            return obj.transmitter.uuid
        except:
            return '-'

    def transmitter_data(self, obj):
        if obj.transmitter:
            redirect_url = reverse('admin:base_transmitter_changelist')
            extra = '{0}'.format(obj.transmitter.pk)
            return '<a href="{0}">Transmitter Initial Data</a>'.format(
                redirect_url + extra)
        else:
            return '-'
    transmitter_data.allow_tags = True


@admin.register(Telemetry)
class TelemetryAdmin(admin.ModelAdmin):
    list_display = ('name', 'decoder')


@admin.register(DemodData)
class DemodDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'satellite', 'source', 'station')
    search_fields = ('transmitter__uuid', 'satellite__norad_cat_id', 'observer')

    def satellite(self, obj):
        return obj.satellite
