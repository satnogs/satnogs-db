from django.core.management.base import BaseCommand

from db.base.models import Satellite, Telemetry, DemodData


class Command(BaseCommand):
    help = 'Decode Satellite data'

    def handle(self, *args, **options):
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
                            payload_decoded = decoder.decode_payload(frame, obj.data_id,
                                                                     obj.timestamp)
                        except:
                            continue

                        obj.payload_decoded = payload_decoded
                        obj.payload_telemetry = option
                        obj.save()
