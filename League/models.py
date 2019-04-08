from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from Accounts.models import Profile
from Scores.models import Mix

DIVISION_CHOICES = [
    ('M', 'Master'),
    ('U', 'Upper Expert'),
    ('L', 'Lower Expert'),
    ('N', 'Novice')
]


class LeagueManager(models.Manager):
    """A League manager"""

    @staticmethod
    def enter_league(event, entry, div=None):
        """Enters someone into a League
        :param event: The League in question
        :param entry: The user entered into it
        :param div: The division as an int?
        :return:
        """
        if div is None:
            div = 2
        rel = LeagueEntry.tourneys.get_or_create(tourney=event, entrants=entry, division=div)
        return rel

    def __str__(self):
        return "{} - {} - {}".format(self.tourney.name, self.entrants.rival_code, self.division)


class League(models.Model):
    """Model for the Leagues"""
    name = models.CharField(max_length=100)
    organizer = models.OneToOneField(User, on_delete=models.CASCADE)
    mix = models.OneToOneField(Mix, on_delete=models.CASCADE)
    location = models.TextField(max_length=5000, help_text="Street, City, State, Zip Code, Country, Planet.")
    rules = models.TextField(max_length=10000, help_text="Detail all of the rules of your League here.")
    competition_date = models.DateField(default=timezone.now)

    def __str__(self):
        return "{}, {}".format(self.name, self.location)


class LeagueResult(models.Model):
    league = models.ForeignKey(League, models.CASCADE)
    winner = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='winner')
    second = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='second_place')
    third = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='third_place')

    def __str__(self):
        return "{}".format(self.league.name)


class LeagueEntry(models.Model):
    league = models.ForeignKey(League, models.CASCADE)
    entrants = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='entrant')
    division = models.CharField(choices=DIVISION_CHOICES, max_length=1)

    tourneys = LeagueManager()
