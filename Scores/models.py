from django.db import models
from django.urls import reverse

from Accounts.models import Profile


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/proof_{1}'.format(instance.player.id, filename)


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
    min_bpm = models.IntegerField()
    max_bpm = models.IntegerField(null=True)
    beg = models.IntegerField(null=True)
    bsp = models.IntegerField(null=True)
    dsp = models.IntegerField(null=True)
    esp = models.IntegerField(null=True)
    csp = models.IntegerField(null=True)
    bdp = models.IntegerField(null=True)
    ddp = models.IntegerField(null=True)
    edp = models.IntegerField(null=True)
    cdp = models.IntegerField(null=True)
    beg_steps = models.IntegerField(default=0)
    bsp_steps = models.IntegerField(default=0)
    dsp_steps = models.IntegerField(default=0)
    esp_steps = models.IntegerField(default=0)
    csp_steps = models.IntegerField(default=0)
    bdp_steps = models.IntegerField(default=0)
    ddp_steps = models.IntegerField(default=0)
    edp_steps = models.IntegerField(default=0)
    cdp_steps = models.IntegerField(default=0)
    beg_holds = models.IntegerField(default=0)
    bsp_holds = models.IntegerField(default=0)
    dsp_holds = models.IntegerField(default=0)
    esp_holds = models.IntegerField(default=0)
    csp_holds = models.IntegerField(default=0)
    bdp_holds = models.IntegerField(default=0)
    ddp_holds = models.IntegerField(default=0)
    edp_holds = models.IntegerField(default=0)
    cdp_holds = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"

    def bpm(self):
        if self.min_bpm == self.max_bpm:
            return f"{self.min_bpm}"
        else:
            return f"{self.min_bpm} - {self.max_bpm}"


class Score(models.Model):
    song = models.ForeignKey(Song, models.CASCADE)
    player = models.ForeignKey(Profile, models.CASCADE)
    difficulty = models.CharField(max_length=3)
    marvelous = models.IntegerField()
    perfect = models.IntegerField()
    great = models.IntegerField()
    good = models.IntegerField()
    OK = models.IntegerField()
    miss = models.IntegerField()
    proof = models.ImageField(upload_to=user_directory_path)
    date = models.DateTimeField(auto_now_add=True)

    def song_list(self, argument):
        song_type = {
            "BEG": self.song.beg_steps + self.song.beg_holds,
            "BSP": self.song.bsp_steps + self.song.bsp_holds,
            "DSP": self.song.dsp_steps + self.song.dsp_holds,
            "ESP": self.song.esp_steps + self.song.esp_holds,
            "CSP": self.song.csp_steps + self.song.csp_holds,
            "BDP": self.song.bdp_steps + self.song.bdp_holds,
            "DDP": self.song.ddp_steps + self.song.ddp_holds,
            "EDP": self.song.edp_steps + self.song.edp_holds,
            "CDP": self.song.cdp_steps + self.song.cdp_holds
        }
        return song_type.get(argument, 0)

    def ex_check(self):
        tip = self.difficulty
        steps = Score.song_list(self, tip)

        num_steps = (self.marvelous + self.perfect + self.great + self.good + self.OK + self.miss)
        if num_steps != steps:
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
        tip = self.difficulty
        steps = Score.song_list(self, tip)

        if (steps + self.OK) == 0:
            reg_score = 0
            return reg_score
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

    def get_absolute_url(self):
        return reverse('Scores:score-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.song}, {self.player}"
