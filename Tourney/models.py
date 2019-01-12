from django.contrib.auth.models import User
from django.db import models

from Accounts.models import Profile
from Scores.models import Mix

DIVISION_CHOICES = [
    ('M', 'Master'),
    ('U', 'Upper Expert'),
    ('L', 'Lower Expert')
]


class Prize(models.Model):
    title: models.CharField(max_length=50)
    place1: models.IntegerField()
    place2: models.IntegerField()
    place3: models.IntegerField()
    place4: models.IntegerField()


class Tournament(models.Model):
    name: models.CharField(max_length=100)
    organizer: models.OneToOneField(User, on_delete=models.CASCADE)
    mix: models.OneToOneField(Mix, on_delete=models.CASCADE)
    location: models.TextField(max_length=5000, help_text="Street, City, State, Zip Code, Country, Planet.")
    rules: models.TextField(max_length=10000, help_text="Detail all of the rules of your tournament here.")
    prize_Pool: models.ForeignKey(Prize, models.CASCADE)
    Date: models.DateField()


class TournamentResult(models.Model):
    tourney: models.ForeignKey(Tournament, models.CASCADE)
    entrants: models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    winner: models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    second: models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    third: models.ForeignKey(Profile, on_delete=models.DO_NOTHING)


class TournamentEntry(models.Model):
    tourney: models.ForeignKey(Tournament, models.CASCADE)
    entrants: models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    division: models.CharField(choices=DIVISION_CHOICES, max_length="1")
