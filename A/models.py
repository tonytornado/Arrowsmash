from django.contrib.auth.models import User
from django.db import models


class Prizes(models.Model):
    Title: models.CharField(max_length=50)
    Place1: models.IntegerField()
    Place2: models.IntegerField()
    Place3: models.IntegerField()
    Place4: models.IntegerField()


class Tournament(models.Model):
    Name: models.CharField(max_length=100)
    Organizer: models.OneToOneField(User, on_delete=models.CASCADE)
    Location: models.TextField(max_length=5000, help_text="Street, City, State, Zip Code, Country, Planet.")
    Rules: models.TextField(max_length=10000, help_text="Detail all of the rules of your tournament here.")
    Prize_Pool: models.ForeignKey(Prizes, models.CASCADE, related_name="title", to_field="Title")
