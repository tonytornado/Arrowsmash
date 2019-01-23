import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

GENDER_CHOICES = (
    ["NB", "Non-Binary"],
    ["GQ", "Gender-fluid"],
    ["M", "Male"],
    ["F", "Female"],
    ["TM", "Trans-Male"],
    ["TF", "Trans-Female"]
)

FRIENDSHIP_STATUS = (
    ['P', 'PENDING'],
    ['A', 'ACCEPTED'],
    ['D', 'DENIED'],
    ['B', 'BLOCKED']
)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    """
    Main profile class that needs all the work.
    """
    user = models.OneToOneField(User, models.CASCADE)
    avatar = models.ImageField(upload_to=user_directory_path, default='default.jpg')
    rival_code = models.CharField(max_length=9, blank=True)
    tagline = models.CharField(max_length=100, blank=True, help_text="It's your life. What's its tag line?")
    DOB = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, default="NB", max_length=2, help_text='We have to ask.')
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=2, blank=True)
    bio = models.TextField(max_length=5000, blank=True)

    @property
    def age(self):
        return datetime.date.today().year - self.DOB.year

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    @staticmethod
    def get_friendships():
        friendships = Friend.objects.all()
        return friendships

    def __str__(self):
        return "{} [{} {}]".format(self.user, self.user.first_name, self.user.last_name)


class Friend(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name="usersfriend")
    friendo = models.ForeignKey(User, models.CASCADE, related_name="friendsfriend")
    status = models.CharField(choices=FRIENDSHIP_STATUS, max_length=1)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Friends'

    @classmethod
    def make_friend(cls, pitcher, catcher, status):
        friend, created = cls.objects.get_or_create(
            creator=pitcher, new_friend=catcher, status=status)
        friend.save()

    @classmethod
    def accept_friend(cls, pitcher, catcher, status):
        friend, created = cls.objects.get_or_create(
            creator=pitcher, new_friend=catcher, status=status)
        friend.save()

    @classmethod
    def remove_friend(cls, pitcher, catcher):
        friend = Friend.objects.filter(user__friendsfriend=catcher, status='A')
        friend.delete()
