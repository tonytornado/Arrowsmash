from django.db import models
from django.urls import reverse

from Accounts.models import Profile, user_directory_path

DIFFICULTY_RATING = (
    ("B", "BEGINNER"),
    ('L', 'LIGHT'),
    ('D', 'DIFFICULT'),
    ('E', 'EXPERT'),
    ('C', 'CHALLENGE'),
)

SCORE_RANK = [
    ('AAA', 'AAA'),
    ('AA', 'AA'),
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
]


class Mix(models.Model):
    name = models.CharField(max_length=150)
    year = models.IntegerField()

    @staticmethod
    def song_count():
        return Song.objects.count()

    def __str__(self):
        return "{} - {}".format(self.name, self.year)


class Song(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    bpm = models.IntegerField()
    difficulty = models.CharField(choices=DIFFICULTY_RATING, max_length=1)
    rating = models.IntegerField()
    steps = models.IntegerField()
    folder = models.ForeignKey(Mix, models.CASCADE)

    def __str__(self):
        return "{} [{}] - {}".format(self.name, self.difficulty, self.folder.name)


class Score(models.Model):
    song = models.ForeignKey(Song, models.CASCADE)
    player = models.ForeignKey(Profile, models.CASCADE)
    score_rank = models.CharField(choices=SCORE_RANK, max_length=3)
    max_combo = models.IntegerField()
    marvelous = models.IntegerField()
    perfect = models.IntegerField()
    great = models.IntegerField()
    good = models.IntegerField()
    OK = models.IntegerField()
    miss = models.IntegerField()
    proof = models.ImageField(upload_to=user_directory_path)
    date = models.DateTimeField(auto_now_add=True)

    def ex(self):
        return self.marvelous * 2 + self.perfect * 2 + self.great * 1 + self.OK * 6 - self.miss * 8

    def full_score(self):
        return (self.marvelous * 100) + ((self.perfect * 100) - 10) + ((self.great * 60) - 10) \
               + (self.OK * 100) - self.miss * 100

    def get_absolute_url(self):
        return reverse('Scores:score-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return "{}, {}".format(self.song, self.player)
