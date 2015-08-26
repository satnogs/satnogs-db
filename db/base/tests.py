from django.contrib.auth.models import User

import factory
from factory import fuzzy

from db.base.models import Mode, Satellite, Transmitter, Suggestion


class ModeFactory(factory.django.DjangoModelFactory):
    """Antenna model factory."""
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
    transmitter = factory.SubFactory('db.base.tests.TransmitterFactory')
    citation = fuzzy.FuzzyText()
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Suggestion
