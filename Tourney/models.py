from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from Accounts.models import Profile
from Scores.models import Mix

DIVISION_CHOICES = [
    ('M', 'Master'),
    ('U', 'Upper Expert'),
    ('L', 'Lower Expert')
]


class TournamentManager(models.Manager):
    """A tournament manager"""

    @staticmethod
    def enter_tournament(event, entry, div=None):
        """Enters someone into a tournament"""
        if div is None:
            div = 2
        rel = TournamentEntry.tourneys.get_or_create(tourney=event, entrants=entry, division=div)
        return rel

    def __str__(self):
        return "{} - {} - {}".format(self.tourney.name, self.entrants.rival_code, self.division)


class Tournament(models.Model):
    """Model for the Tournaments"""
    name = models.CharField(max_length=100)
    organizer = models.OneToOneField(User, on_delete=models.CASCADE)
    mix = models.OneToOneField(Mix, on_delete=models.CASCADE)
    location = models.TextField(max_length=5000, help_text="Street, City, State, Zip Code, Country, Planet.")
    rules = models.TextField(max_length=10000, help_text="Detail all of the rules of your tournament here.")
    competition_date = models.DateField(default=timezone.now)
    approval_status: models.BooleanField(default=False)

    def verified(self):
        """returns a verified status"""
        if self.approval_status:
            return "Verified"
        else:
            return "pending"


    def __str__(self):
        return "{}, {} [{}]".format(self.name, self.location, self.verified)


class TournamentResult(models.Model):
    tourney = models.ForeignKey(Tournament, models.CASCADE)
    winner = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='winner')
    second = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='second_place')
    third = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='third_place')

    def __str__(self):
        return "{}".format(self.tourney.name)


class TournamentEntry(models.Model):
    tourney = models.ForeignKey(Tournament, models.CASCADE)
    entrants = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='entrant')
    division = models.CharField(choices=DIVISION_CHOICES, max_length=1)

    tourneys = TournamentManager()
