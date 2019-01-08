from django.contrib.auth.models import User
from django.db import models

# Create your models here.
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
    tagline = models.CharField(max_length=100)
    gender = models.CharField(choices=GENDER_CHOICES, default="NB", max_length=2)
    bio = models.TextField(max_length=5000)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    avatar = models.ImageField(upload_to=user_directory_path, default='default.jpg')

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
