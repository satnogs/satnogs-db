from django.core.management.base import BaseCommand

from db.base.models import Satellite, Telemetry, DemodData


class Command(BaseCommand):
    help = 'Decode Satellite data'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('satellite_identifiers',
                            nargs='+',
                            metavar='<Satellite Identifier>')

    def handle(self, *args, **options):
        for item in options['satellite_identifiers']:
            satellites = Satellite.objects.all()
            for satellite in satellites:
                if satellite.has_telemetry_decoders:
                    data = DemodData.objects.filter(satellite=satellite).filter(payload_decoded='')
                    telemetry_decoders = Telemetry.objects.filter(satellite=satellite)

                    for obj in data:
                        for option in telemetry_decoders:
                            decoder_module = 'db.base.decoders.{0}'.format(option.decoder)
                            decoder = __import__(decoder_module, fromlist='.')

                            with open(obj.payload_frame.path) as fp:
                                frame = fp.read()

                            try:
                                payload_decoded = decoder.decode_payload(frame, obj.timestamp,
                                                                         obj.data_id)
                            except ValueError:
                                obj.payload_decoded = ''
                                obj.payload_telemetry = None
                                obj.save()
                                continue
                            else:
                                obj.payload_decoded = payload_decoded
                                obj.payload_telemetry = option
                                obj.save()
                                break
