from django.db import models
# Create your models here.
from django.urls import reverse

from Accounts.models import Profile, user_directory_path

DIFFICULTY_RATING = (
    ("B", "BEGINNER"),
    ('L', 'LIGHT'),
    ('D', 'DIFFICULT'),
    ('E', 'EXPERT'),
    ('C', 'CHALLENGE'),
)


class Mix(models.Model):
    """
    Mix data
    """
    name: models.CharField(max_length=150)
    year: models.IntegerField()

    @staticmethod
    def song_count():
        return Song.objects.count(Mix)


class Song(models.Model):
    """
    Songs data
    """
    name: models.CharField(max_length=100)
    artist: models.CharField(max_length=100)
    bpm: models.IntegerField(max_length=3)
    difficulty: models.CharField(choices=DIFFICULTY_RATING, max_length=1)
    steps: models.IntegerField()
    folder: models.ForeignKey(Mix, models.CASCADE)


class Score(models.Model):
    """
    For logging scores into a linked table.
    """
    song: models.ForeignKey(Song, models.CASCADE)
    player: models.ForeignKey(Profile, models.CASCADE)
    score_rank: models.CharField(max_length=3)
    ex: models.IntegerField()
    proof: models.ImageField(upload_to=user_directory_path)

    def get_absolute_url(self):
        return reverse('Scores:score-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return "{}, {}".format(self.Song, self.Player)
