import pytest

from rest_framework import status
from django.test import TestCase

from db.base.tests import ModeFactory, SatelliteFactory, TransmitterFactory, DemodDataFactory


@pytest.mark.django_db(transaction=True)
class ModeViewApiTest(TestCase):
    """
    Tests the Mode View API
    """
    mode = None

    def setUp(self):
        self.mode = ModeFactory()
        self.mode.save()

    def test_list(self):
        response = self.client.get('/api/modes/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        response = self.client.get('/api/modes/{0}/'.format(self.mode.id),
                                   format='json')
        self.assertContains(response, self.mode.name)


@pytest.mark.django_db(transaction=True)
class SatelliteViewApiTest(TestCase):
    """
    Tests the Satellite View API
    """
    satellite = None

    def setUp(self):
        self.satellite = SatelliteFactory()
        self.satellite.save()

    def test_list(self):
        response = self.client.get('/api/satellites/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        response = self.client.get('/api/satellites/{0}/'.format(self.satellite.norad_cat_id),
                                   format='json')
        self.assertContains(response, self.satellite.name)


@pytest.mark.django_db(transaction=True)
class TransmitterViewApiTest(TestCase):
    """
    Tests the Transmitter View API
    """
    transmitter = None

    def setUp(self):
        self.transmitter = TransmitterFactory()
        self.transmitter.uuid = 'test'
        self.transmitter.save()

    def test_list(self):
        response = self.client.get('/api/transmitters/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        response = self.client.get('/api/transmitters/{0}/'.format(self.transmitter.uuid),
                                   format='json')
        self.assertContains(response, self.transmitter.description)


@pytest.mark.django_db(transaction=True)
class TelemetryViewApiTest(TestCase):
    """
    Tests the Telemetry View API
    """
    datum = None

    def setUp(self):
        self.datum = DemodDataFactory()
        self.datum.save()

    def test_list(self):
        response = self.client.get('/api/telemetry/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        response = self.client.get('/api/telemetry/{0}/'.format(self.datum.id), format='json')
        self.assertContains(response, self.datum.observer)
