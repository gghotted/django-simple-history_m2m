from django.db import models
from simple_history_m2m.models import HistoricalRecords


class Post(models.Model):
    history = HistoricalRecords()


class Person(models.Model):
    like_posts = models.ManyToManyField(Post, 'like_people')

    history = HistoricalRecords()


class NoHistory(models.Model):
    like_posts = models.ManyToManyField(Post)
