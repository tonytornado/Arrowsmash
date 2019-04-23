import datetime

from django.contrib.auth.models import User
from django.db import models

from Accounts.models import Profile
from Scores.models import Mix, Song

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
        return F"{self.tourney.name} - {self.entrants.rival_code} - {self.division}"


class League(models.Model):
    """Model for the Leagues"""
    name = models.CharField(max_length=100)
    organizer = models.OneToOneField(User, on_delete=models.CASCADE)
    mix = models.OneToOneField(Mix, on_delete=models.CASCADE)
    rules = models.TextField(max_length=10000, help_text="Detail all of the rules of your League here.")
    competition_date_start = models.DateField(default=datetime.date.today)
    competition_date_end = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.name}, {self.competition_date_start} - {self.competition_date_end}"


class LeagueResult(models.Model):
    """Model for league results"""
    league = models.ForeignKey(League, models.CASCADE)
    winner = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='winner')
    second = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='second_place')
    third = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='third_place')

    def __str__(self):
        return f"{self.league.name}"


class LeagueEntry(models.Model):
    """Model for league entry results"""
    league = models.ForeignKey(League, models.CASCADE)
    entrants = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='entrant')
    division = models.CharField(choices=DIVISION_CHOICES, max_length=1)

    tourneys = LeagueManager()


class Trial(models.Model):
    """Model for Trial Entry"""
    title = models.CharField(max_length=100)
    deadline = models.DateTimeField()
    division = models.CharField(choices=DIVISION_CHOICES, max_length=1)
    song1 = models.ForeignKey(Song, models.CASCADE, related_name="first_song")
    song2 = models.ForeignKey(Song, models.CASCADE, related_name="second_song")
    song3 = models.ForeignKey(Song, models.CASCADE, related_name="third_song")
    song4 = models.ForeignKey(Song, models.CASCADE, related_name="final_song")

    def __str__(self):
        return f"{self.title} - {self.deadline}"

    def trial_list(self):
        return f"{self.song1.name}, {self.song2.name}, {self.song3.name}, {self.song4.name}"
