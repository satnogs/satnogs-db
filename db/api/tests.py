import pytest

from rest_framework import status
from django.test import TestCase

from db.base.tests import ModeFactory


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
