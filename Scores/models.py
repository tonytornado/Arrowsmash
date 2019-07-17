from django.db import models
from django.urls import reverse

from Accounts.models import Profile


class ChartDifficulty(models.Model):
    difficulty: str = models.CharField(max_length=5)
    step: str = models.CharField(max_length=5)
    shock: str = models.CharField(max_length=5)
    freeze: str = models.CharField(max_length=5)


class ChartLevel(models.Model):
    beginner: ChartDifficulty = models.ForeignKey(ChartDifficulty,
                                                  models.CASCADE,
                                                  related_name="beginner",
                                                  null=True
                                                  )
    basic: ChartDifficulty = models.ForeignKey(ChartDifficulty,
                                               models.CASCADE,
                                               related_name="basic",
                                               null=True
                                               )
    difficult: ChartDifficulty = models.ForeignKey(ChartDifficulty,
                                                   models.CASCADE,
                                                   related_name="difficult",
                                                   null=True
                                                   )
    expert: ChartDifficulty = models.ForeignKey(ChartDifficulty,
                                                models.CASCADE,
                                                related_name="expert",
                                                null=True
                                                )
    challenge: ChartDifficulty = models.ForeignKey(ChartDifficulty,
                                                   models.CASCADE,
                                                   related_name="challenge",
                                                   null=True
                                                   )


class SongChart(models.Model):
    unlock: bool = models.BooleanField(default=False, null=True)
    us_locked: bool = models.BooleanField(default=False, null=True)
    name: str = models.CharField(max_length=100)
    artist: str = models.CharField(max_length=100)
    folder: str = models.CharField(max_length=80, blank=True)
    bpm: str = models.CharField(max_length=20)
    name_translation: str = models.CharField(max_length=100, blank=True)
    artist_translation: str = models.CharField(max_length=100, blank=True)
    genre: str = models.CharField(max_length=50, blank=True)
    single: ChartLevel = models.ForeignKey(ChartLevel, models.CASCADE, related_name="single")
    double: ChartLevel = models.ForeignKey(ChartLevel, models.CASCADE, related_name="double")

    def __str__(self):
        return f"{self.name}"


def user_directory_path(instance, filename):
    """
    Defines the filepath of the user directory
    :param instance:
    :param filename:
    :return:
    """
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'images/user_{instance.player.id}/proof_{filename}'


DIFFICULTY_SELECT = (
    ("1", "BEG"),
    ("2", "BSP"),
    ('3', "DSP"),
    ("4", "ESP"),
    ("5", "CSP"),
    ("6", "BDP"),
    ("7", "DDP"),
    ("8", "EDP"),
)


class Score(models.Model):
    song = models.ForeignKey(SongChart, models.CASCADE, related_name='song')
    player = models.ForeignKey(Profile, models.CASCADE, related_name='player')
    difficulty = models.CharField(choices=DIFFICULTY_SELECT, default=1, max_length=1)
    marvelous = models.IntegerField()
    perfect = models.IntegerField()
    great = models.IntegerField()
    good = models.IntegerField()
    OK = models.IntegerField()
    miss = models.IntegerField()
    proof = models.ImageField(upload_to=user_directory_path)
    date = models.DateTimeField(auto_now_add=True)

    def song_list(self, argument):
        """
        Returns the steps of the current song based on the difficulty
        :param argument: usually set to the difficulty of the song chosen
        :return:
        """
        song_type = {
            "BEG": self.song.single.beginner.step + self.song.single.beginner.freeze,
            "BSP": self.song.single.basic.step + self.song.single.basic.freeze,
            "DSP": self.song.single.difficult.step + self.song.single.difficult.freeze,
            "ESP": self.song.single.expert.step + self.song.single.expert.freeze,
            "CSP": self.song.single.challenge.step + self.song.single.challenge.freeze,
            "BDP": self.song.double.basic.step + self.song.double.basic.freeze,
            "DDP": self.song.double.difficult.step + self.song.double.difficult.freeze,
            "EDP": self.song.double.expert.step + self.song.double.expert.freeze,
            "CDP": self.song.double.challenge.step + self.song.double.challenge.freeze,
        }
        return song_type.get(argument, 0)

    @property
    def ex_check(self):
        """
        Checks the EX score of a song to validate the score having correct steps/jumps/shocks
        :return:
        """
        tip = self.difficulty
        steps = Score.song_list(self, tip)

        num_steps = (self.marvelous + self.perfect + self.great + self.good + self.OK + self.miss)
        return True if num_steps == steps else False

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
        tip = self.difficulty
        steps = Score.song_list(self, tip)

        if (steps + self.OK) == 0:
            return "N/A"
        else:
            num_steps = self.marvelous + self.perfect + self.great + self.good + self.miss
            marv_score = 1000000 / (steps + self.OK)
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
                return "Blue [Good Full Combo]"
        else:
            return False

    @property
    def letter_grade(self):
        """
        Returns a letter grade for the song
        :return:
        """
        if self.full_score is int:
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
                return "D / E"
        else:
            return "N/A"

    def get_absolute_url(self):
        return reverse('Scores:score-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.song}, {self.player}"
