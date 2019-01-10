import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

GENDER_CHOICES = (
    ("NB", "Non-Binary"),
    ["M", "Male"],
    ("F", "Female"),
)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    avatar = models.ImageField(upload_to=user_directory_path, default='default.jpg',
                               help_text='Show your face, if you would.')
    rival_code = models.CharField(max_length=9, blank=True)
    tagline = models.CharField(max_length=100, blank=True)
    DOB = models.DateField(help_text='When were you born?', blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, default="NB", max_length=2)
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
