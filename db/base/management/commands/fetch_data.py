import requests
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.conf import settings

from db.base.models import Satellite, Transmitter, DemodData


class Command(BaseCommand):
    help = 'Fetch and decode Satellite data from Network'

    def handle(self, *args, **options):
        apiurl = settings.NETWORK_API_ENDPOINT
        data_url = "{0}data".format(apiurl)
        start_date = datetime.utcnow() - timedelta(days=int(settings.DATA_FETCH_DAYS))
        start_date = datetime.strftime(start_date, '%Y-%m-%dT%H:%M:%SZ')
        params = {'start': start_date}
        response = requests.get(data_url, params=params)

        satellites = Satellite.objects.exclude(telemetry_decoder__exact='')

        for obj in response.json():
            norad_cat_id = obj['norad_cat_id']
            data_id = obj['id']
            try:
                satellite = satellites.get(norad_cat_id=norad_cat_id)
            except Satellite.DoesNotExist:
                continue
            try:
                transmitter = Transmitter.objects.get(uuid=obj['transmitter'])
            except Transmitter.DoesNotExist:
                continue
            demoddata = DemodData.objects.filter(data_id=data_id).delete()

            decoder_module = 'db.base.decoders.{0}'.format(satellite.telemetry_decoder)
            decoder = __import__(decoder_module, fromlist='.')

            for demoddata in obj['demoddata']:
                payload_url = demoddata['payload_demod']
                observation_datetime = payload_url.split('/')[-1]
                payload = str(requests.get(payload_url).json())
                telemetry = decoder.decode_payload(payload, observation_datetime, data_id)
                for item in telemetry:
                    DemodData.objects.create(payload=item, transmitter=transmitter,
                                             data_id=data_id)
