# Create your models here.

# DIFFICULTY_RATING = (
#     ("B", "BEGINNER"),
#     ('L', 'LIGHT'),
#     ('D', 'DIFFICULT'),
#     ('E', 'EXPERT'),
#     ('C', 'CHALLENGE'),
# )
#
#
# class Album(models.Model):
#     Name: models.CharField(max_length=150)
#     Year: models.IntegerField()
#
#     @staticmethod
#     def song_count():
#         return Song.objects.count(Song.Mix)
#
#
# class Song(models.Model):
#     Name: models.CharField(max_length=100)
#     Artist: models.CharField(max_length=100)
#     BPM: models.IntegerField(max_length=3)
#     Difficulty: models.CharField(choices=DIFFICULTY_RATING, max_length=1)
#     Steps: models.IntegerField()
#     Mix: models.ForeignKey(Album, models.CASCADE)
#
#
# class Score(models.Model):
#     song: models.ForeignKey(Song, models.CASCADE)
#     player: models.ForeignKey(Profile, models.CASCADE)
