import pytest

from rest_framework import status
from django.test import TestCase

from db.base.tests import ModeFactory, SatelliteFactory, TransmitterFactory


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
        response = self.client.get('/api/modes/%s/' % self.mode.id)
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
        response = self.client.get('/api/satellites/%s/' % self.satellite.norad_cat_id)
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
        response = self.client.get('/api/transmitters/%s/' % self.transmitter.uuid)
        self.assertContains(response, self.transmitter.description)
