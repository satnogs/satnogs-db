from django.contrib.auth.models import User

import factory
from factory import fuzzy

from db.base.models import MODE_CHOICES, Satellite, Transponder, Suggestion


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


class TransponderFactory(factory.django.DjangoModelFactory):
    """Transponder model factory."""
    description = fuzzy.FuzzyText()
    alive = fuzzy.FuzzyChoice(choices=[True, False])
    uplink_low = fuzzy.FuzzyInteger(200000000, 500000000, step=10000)
    uplink_high = fuzzy.FuzzyInteger(200000000, 500000000, step=10000)
    downlink_low = fuzzy.FuzzyInteger(200000000, 500000000, step=10000)
    downlink_high = fuzzy.FuzzyInteger(200000000, 500000000, step=10000)
    mode = fuzzy.FuzzyChoice(choices=MODE_CHOICES)
    invert = fuzzy.FuzzyChoice(choices=[True, False])
    baud = fuzzy.FuzzyInteger(4000, 22000, step=1000)
    satellite = factory.SubFactory(SatelliteFactory)

    class Meta:
        model = Transponder


class SuggestionFactory(factory.django.DjangoModelFactory):
    transponder = factory.SubFactory('db.base.tests.TransponderFactory')
    citation = fuzzy.FuzzyText()
    user = factory.SubFactory('db.base.tests.UserFactory')

    class Meta:
        model = Suggestion
