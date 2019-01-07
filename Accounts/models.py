from django.contrib.auth import logout
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


class Profile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    tagline = models.CharField(max_length=100)
    gender = models.CharField(choices=GENDER_CHOICES, default="NB", max_length=2)
    bio = models.TextField(max_length=5000)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()