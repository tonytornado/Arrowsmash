import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

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
    return f"images/user_{instance.user.id}/{filename}"


class Profile(models.Model):
    """    Main profile class that needs all the work.    """
    user = models.OneToOneField(User, models.CASCADE)
    avatar = models.ImageField(upload_to=user_directory_path, default='images/default.jpg')
    rival_code = models.CharField(max_length=9, blank=True)
    tagline = models.CharField(max_length=100, blank=True, help_text="It's your life. What's its tag line?")
    DOB = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, default="NB", max_length=2, help_text='We have to ask.')
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=2, blank=True)
    bio = models.TextField(max_length=5000, blank=True)

    objects = models.Manager()

    @property
    def age(self):
        """Returns the age of a user"""
        if self.DOB:
            return datetime.date.today().year - self.DOB.year
        else:
            return "N/A"

    @property
    def full_name(self):
        """Returns a full name"""
        return "{} {}".format(self.user.first_name, self.user.last_name)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        """Updates the profile for someone"""
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        """Saves the profile for someone"""
        instance.profile.save()

    def __str__(self):
        return "{} [{} {}]".format(self.user, self.user.first_name, self.user.last_name)


class FollowManager(models.Manager):
    """Follower Management"""

    @staticmethod
    def follow(follower, followee):
        """
        Follow someone
        :param follower: That's you!
        :param followee: That's who you want to follow.
        :return:
        """
        if follower == followee:
            raise ValidationError("You can't follow yourself... seriously.")

        relation, created = Follow.objects \
            .get_or_create(follower=follower, followee=followee)

        if created is False:
            raise ValueError("You're already following them")

        return relation

    @staticmethod
    def remove_follow(follower, followee):
        """
        Removes a follow, obviously
        :param follower:
        :param followee:
        :return:
        """
        if follower == followee:
            raise ValidationError("You can't unfollow yourself... why?")

        try:
            rel = Follow.objects \
                .get(follower=follower, followee=followee)
            rel.delete()
            return True
        except Follow.DoesNotExist:
            return False

    @staticmethod
    def following_set(pro):
        qs = Follow.objects.filter(follower=pro).all()
        following = [u.followee for u in qs]
        return following

    @staticmethod
    def followers_set(pro):
        qs = Follow.objects.filter(followee=pro).all()
        followers = [u.follower for u in qs]
        return followers


class Follow(models.Model):
    """ Model to represent Following relationships """
    follower = models.ForeignKey(Profile, models.CASCADE, related_name='stalker')
    followee = models.ForeignKey(Profile, models.CASCADE, related_name='stalked')
    created = models.DateTimeField(default=timezone.now)

    objects = FollowManager()

    def __str__(self):
        return "Player #%s follows #%s" % (self.follower.user.pk, self.followee.user.pk)

    def save(self, *args, **kwargs):
        # Ensure users can't be friends with themselves
        if self.follower == self.followee:
            raise ValidationError("Users cannot follow themselves.")
        super(Follow, self).save(*args, **kwargs)
