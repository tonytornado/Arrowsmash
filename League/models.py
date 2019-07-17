from datetime import datetime, date
from typing import Tuple

from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.files import ImageFieldFile

from Accounts.models import Profile
from Scores.models import SongChart

DIVISION_CHOICES = [
    ('M', 'Master'),
    ('U', 'Upper Expert'),
    ('L', 'Lower Expert'),
    ('N', 'Novice')
]


class LeagueManager(models.Manager):
    """League manager"""

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
        rel = LeagueEntry.objects.get_or_create(tourney=event, entrants=entry, division=div)
        return rel

    def __str__(self):
        return F"{self.tourney.name} - {self.entrants.rival_code} - {self.division}"


class League(models.Model):
    """Model for the Leagues"""
    name: str = models.CharField(max_length=100)
    organizer: User = models.OneToOneField(User, on_delete=models.CASCADE)
    rules: str = models.TextField(max_length=10000, help_text="Detail all of the rules of your League here.")
    competition_date_start: date = models.DateField(default=datetime.now)
    competition_date_end: date = models.DateField(default=datetime.now)

    @property
    def __str__(self):
        return f"{self.name}, {self.competition_date_start} - {self.competition_date_end}"


class LeagueResult(models.Model):
    """Model for league results display"""
    league: League = models.ForeignKey(League, models.CASCADE)
    winner: Profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='winner')
    second: Profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='second_place')
    third: Profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='third_place')

    @property
    def __str__(self):
        return f"{self.league.name}"


class LeagueEntry(models.Model):
    """Model for league entry results"""
    league: League = models.ForeignKey(League, models.CASCADE)
    entrants: Profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='entrant')
    division: str = models.CharField(choices=DIVISION_CHOICES, max_length=1)

    federation: LeagueManager = LeagueManager()


class TrialManager(models.Manager):
    """Trial management"""

    @staticmethod
    def start_trial(event, dancer):
        """
        For adding a trial.
        :param event: Trial itself.
        :param dancer: The profile of the player taking it on.
        :return:
        """
        rel: Tuple[TrialEntry, bool] = TrialEntry.objects.get_or_create(trial=event, player=dancer)
        return rel


class Trial(models.Model):
    """Model for Trials"""
    title: str = models.CharField(max_length=100)
    deadline: datetime = models.DateTimeField()
    division: str = models.CharField(choices=DIVISION_CHOICES, max_length=1)
    song1: SongChart = models.ForeignKey(SongChart, models.CASCADE, related_name="first_song")
    song2: SongChart = models.ForeignKey(SongChart, models.CASCADE, related_name="second_song")
    song3: SongChart = models.ForeignKey(SongChart, models.CASCADE, related_name="third_song")
    song4: SongChart = models.ForeignKey(SongChart, models.CASCADE, related_name="final_song")
    art: ImageFieldFile = models.ImageField(null=True, blank=True, upload_to='images/trial_art')

    def __str__(self):
        return f"{self.title} - {self.deadline}"

    @property
    def trial_list(self):
        """
        Returns a list name for the trials.
        :return:
        """
        return f"{self.song1.name}, {self.song2.name}, {self.song3.name}, {self.song4.name}"


class TrialEntry(models.Model):
    """Model for trial entry"""
    trial: Trial = models.ForeignKey(Trial, models.CASCADE, related_name="challenge")
    player: Profile = models.ForeignKey(Profile, models.CASCADE, related_name="challenger")

    objects: TrialManager = TrialManager()
