from django.db import models
from django.urls import reverse

from Accounts.models import Profile

DIFFICULTY_RATING = (
    ("B", "BEGINNER"),
    ('L', 'LIGHT'),
    ('D', 'DIFFICULT'),
    ('E', 'EXPERT'),
    ('C', 'CHALLENGE'),
)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}_proof'.format(instance.player.id, filename)


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
    player = models.ForeignKey(Profile, models.CASCADE, related_name='dancer')
    marvelous = models.IntegerField()
    perfect = models.IntegerField()
    great = models.IntegerField()
    good = models.IntegerField()
    OK = models.IntegerField()
    miss = models.IntegerField()
    proof = models.ImageField(upload_to=user_directory_path)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def ex_check(self):
        num_steps = (self.marvelous + self.perfect + self.great + self.good + self.OK + self.miss)
        if num_steps != self.song.steps:
            return False
        else:
            return True

    @property
    def ex(self):
        """
        Returns the EX score for the song.
        :return:
        """
        score = (self.marvelous * 3) + (self.perfect * 2) + (self.great * 1) + (self.OK * 3)
        return score

    @property
    def full_score(self):
        """
        Returns the full number score of the song
        :return:
        """
        num_steps = self.marvelous + self.perfect + self.great + self.good + self.miss
        marv_score = 1000000 / (self.song.steps + self.OK)
        perf_score = marv_score - 10
        great_score = (marv_score * 0.6) - 10
        good_score = (marv_score * 0.2) - 10
        reg_score = ((marv_score * (self.marvelous + self.OK) + (perf_score * self.perfect) + (
                great_score * self.great) + (
                              good_score * self.good) + 0.1) / 10) * 10
        if num_steps != 0:
            return round(reg_score)

    @property
    def full_combo(self):
        """
        Shows the special text for full combos.
        :return:
        """
        if self.miss == 0:
            if self.good == 0:
                if self.great == 0:
                    if self.perfect == 0:
                        if self.marvelous == 0:
                            pass
                        else:
                            return "You are Supreme!"
                    else:
                        return "Yellow [Perfect Full Combo]"
                else:
                    return "Green [Great Full Combo]"
            else:
                return "Blue [Good Full Combo"
        else:
            return False

    @property
    def letter_grade(self):
        """
        Returns a letter grade for the song
        :return:
        """
        if self.full_score >= 990000:
            return "AAA"
        if 950000 <= self.full_score <= 989990:
            return "AA+"
        if 900000 <= self.full_score <= 949990:
            return "AA"
        if 890000 <= self.full_score <= 899990:
            return "AA-"
        if 850000 <= self.full_score <= 889990:
            return "A+"
        if 800000 <= self.full_score <= 849990:
            return "A"
        if 790000 <= self.full_score <= 799990:
            return "A-"
        if 750000 <= self.full_score <= 789990:
            return "B+"
        if 700000 <= self.full_score <= 749990:
            return "B"
        if 690000 <= self.full_score <= 699990:
            return "B-"
        if 650000 <= self.full_score <= 689990:
            return "C+"
        if 600000 <= self.full_score <= 649990:
            return "C"
        if 590000 <= self.full_score <= 599990:
            return "C-"
        if 550000 <= self.full_score <= 589990:
            return "D+"
        if 0 <= self.full_score <= 549990:
            return "D"

    def get_absolute_url(self):
        return reverse('Scores:score-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return "{}, {}".format(self.song, self.player)
