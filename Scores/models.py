from django.db import models

# Create your models here.
from Accounts.models import Profile, user_directory_path

DIFFICULTY_RATING = (
    ("B", "BEGINNER"),
    ('L', 'LIGHT'),
    ('D', 'DIFFICULT'),
    ('E', 'EXPERT'),
    ('C', 'CHALLENGE'),
)

SCORE_RANK = (
    "AAA",
    "AA",
    'A',
    'B',
    'C',
    'D',
    'E',
)


class Mix(models.Model):
    """
    Mix data
    """
    Name: models.CharField(max_length=150)
    Year: models.IntegerField()

    @staticmethod
    def song_count():
        return Song.objects.count(Mix)


class Song(models.Model):
    """
    Songs data
    """
    Name: models.CharField(max_length=100)
    Artist: models.CharField(max_length=100)
    BPM: models.IntegerField(max_length=3)
    Difficulty: models.CharField(choices=DIFFICULTY_RATING, max_length=1)
    Steps: models.IntegerField()
    Folder: models.ForeignKey(Mix, models.CASCADE)


class Score(models.Model):
    """
    For logging scores into a linked table.
    """
    song: models.ForeignKey(Song, models.CASCADE)
    player: models.ForeignKey(Profile, models.CASCADE)
    score_rank: models.CharField(choices=SCORE_RANK, max_length=3)
    EX: models.IntegerField()
    Proof: models.ImageField(upload_to=user_directory_path)
