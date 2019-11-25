from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=20)

class Movie(models.Model):
    title = models.CharField(max_length=30)
    poster_url = models.CharField(max_length=140)
    description = models.TextField()
    genres = models.ManyToManyField(
        Genre,
        related_name='movies_genre',
        blank=True
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_movies',
        blank=True
    )
    rate_avg = models.FloatField()
    release_date = models.DateField()
    movie_id = models.IntegerField()
    grade = models.IntegerField()
    view_img = models.CharField(max_length=140)
    rate_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='rate_movies',
        through='Score',
        blank=True
    )

class Score(models.Model):
    score = models.IntegerField(default=0)
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    

class Review(models.Model):
    content = models.CharField(max_length=140)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

