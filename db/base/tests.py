import random
from datetime import datetime, timedelta
import pytest

import factory
from factory import fuzzy
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import now

from db.base.models import (DATA_SOURCES, Mode, Satellite, Transmitter, Suggestion,
                            Telemetry, DemodData)


DATA_SOURCE_IDS = [c[0] for c in DATA_SOURCES]


def generate_payload():
    payload = '{0:b}'.format(random.randint(500000000, 510000000))
    digits = 1824
    while digits:
        digit = random.randint(0, 1)
        payload += str(digit)
        digits -= 1
    return payload


def generate_payload_name():
    filename = datetime.strftime(fuzzy.FuzzyDateTime(now() - timedelta(days=10), now()).fuzz(),
                                 '%Y%m%dT%H%M%SZ')
    return filename


def get_valid_satellites():
    qs = Transmitter.objects.all()
    satellites = Satellite.objects.filter(transmitters__in=qs).distinct()
    return satellites


class ModeFactory(factory.django.DjangoModelFactory):
    """Mode model factory."""
    name = fuzzy.FuzzyText()

    class Meta:
        model = Mode


class UserFactory(factory.django.DjangoModelFactory):
    """User model factory"""
    username = factory.Sequence(lambda n: "user_%d" % n)

    class Meta:
        model = User


class SatelliteFactory(factory.django.DjangoModelFactory):
    """Sattelite model factory."""
    norad_cat_id = fuzzy.FuzzyInteger(2000, 4000)
    name = fuzzy.FuzzyText()

    class Meta:
        model = Satellite


class TransmitterFactory(factory.django.DjangoModelFactory):
    """Transmitter model factory."""
    description = fuzzy.FuzzyText()
    alive = fuzzy.FuzzyChoice(choices=[True, False])
    uplink_low = fuzzy.FuzzyInteger(200000000, 500000000, step=10000)
    uplink_high = fuzzy.FuzzyInteger(200000000, 500000000, step=10000)
    downlink_low = fuzzy.FuzzyInteger(200000000, 500000000, step=10000)
    downlink_high = fuzzy.FuzzyInteger(200000000, 500000000, step=10000)
    mode = factory.SubFactory(ModeFactory)
    invert = fuzzy.FuzzyChoice(choices=[True, False])
    baud = fuzzy.FuzzyInteger(4000, 22000, step=1000)
    satellite = factory.SubFactory(SatelliteFactory)
    approved = fuzzy.FuzzyChoice(choices=[True, False])

    class Meta:
        model = Transmitter


class SuggestionFactory(factory.django.DjangoModelFactory):
    transmitter = factory.SubFactory(TransmitterFactory)
    citation = fuzzy.FuzzyText()
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Suggestion


class TelemetryFactory(factory.django.DjangoModelFactory):
    satellite = factory.SubFactory(SatelliteFactory)
    name = fuzzy.FuzzyText()
    schema = '{}'
    decoder = 'qb50'

    class Meta:
        model = Telemetry


class DemodDataFactory(factory.django.DjangoModelFactory):
    satellite = factory.SubFactory(SatelliteFactory)
    transmitter = factory.SubFactory(TransmitterFactory)
    source = fuzzy.FuzzyChoice(choices=DATA_SOURCE_IDS)
    data_id = fuzzy.FuzzyInteger(0, 200)
    payload_frame = factory.django.FileField(filename='data.raw')
    payload_decoded = '{}'
    payload_telemetry = factory.SubFactory(TelemetryFactory)
    station = fuzzy.FuzzyText()
    lat = fuzzy.FuzzyFloat(-20, 70)
    lng = fuzzy.FuzzyFloat(-180, 180)
    timestamp = fuzzy.FuzzyDateTime(now() - timedelta(days=10), now())

    class Meta:
        model = DemodData


@pytest.mark.django_db(transaction=True)
class HomeViewTest(TestCase):
    """
    Simple test to make sure the home page is working
    """
    def test_home_page(self):
        response = self.client.get('/')
        self.assertContains(response, 'SatNOGS DB is, and will always be, an open database.')


@pytest.mark.django_db(transaction=True)
class SatelliteViewTest(TestCase):
    """
    Test to make sure the satellite page is working
    """
    satellite = None

    def setUp(self):
        self.satellite = SatelliteFactory()
        self.satellite.save()

    def test_satellite_page(self):
        response = self.client.get('/satellite/%s/' % self.satellite.norad_cat_id)
        self.assertContains(response, self.satellite.name)


@pytest.mark.django_db(transaction=True)
class AboutViewTest(TestCase):
    """
    Test to make sure the about page is working
    """
    def test_about_page(self):
        response = self.client.get('/about/')
        self.assertContains(response, 'SatNOGS DB is an effort to create an hollistic')


@pytest.mark.django_db(transaction=True)
class FaqViewTest(TestCase):
    """
    Test to make sure the faq page is working
    """
    def test_faq_page(self):
        response = self.client.get('/faq/')
        self.assertContains(response, 'How do I suggest a new transmitter?')


@pytest.mark.django_db(transaction=True)
class StatsViewTest(TestCase):
    """
    Test to make sure the stats page is working
    """
    def test_stats_page(self):
        response = self.client.get('/stats/')
        self.assertContains(response, 'Total satellites')
