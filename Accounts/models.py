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

    @property
    def get_follow_status(request):
        return Follow.objects.get(follower=request.user.pk)

    def __str__(self):
        return "{} [{} {}]".format(self.user, self.user.first_name, self.user.last_name)


class Follow(models.Model):
    """ Model to represent Following relationships """
    follower = models.ForeignKey(Profile, models.CASCADE, related_name='following')
    followee = models.ForeignKey(Profile, models.CASCADE, related_name='followers')
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Player #%s follows #%s" % (self.follower.user.username, self.followee.user.username)

    def save(self, *args, **kwargs):
        # Ensure users can't be friends with themselves
        if self.follower == self.followee:
            raise ValidationError("Users cannot follow themselves.")
        super(Follow, self).save(*args, **kwargs)

    @staticmethod
    def follow(follower, followee):
        if follower == followee:
            raise ValidationError("You can't follow yourself... seriously.")

        relation, created = Follow.objects \
            .get_or_create(follower=follower, followee=followee)

        if created is False:
            raise ValueError("You're already following them")

        return relation

    @staticmethod
    def remove_follow(follower, followee):
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
