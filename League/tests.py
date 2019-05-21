# Create your tests here.
from datetime import date

from django.test import TestCase

from League.models import Trial


class TrialTestCase(TestCase):
    @staticmethod
    def set_up():
        Trial.objects.create(title="One", deadline=date(2019, 10, 10), division="M", song1_id=120, song2_id=11,
                             song3_id=12, song4_id=89)

    def test_trial(self):
        trial = Trial.objects.get(title="One")
        self.assertIsNotNone(trial.division, "This is a valid division")
