from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    author = models.ForeignKey(User, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    msg = JSONField()


class MobilePushToken(models.Model):
    user = models.ForeignKey(User, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    token = models.TextField()


class Room(models.Model):
    creator = models.ForeignKey(User, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=64)
    is_private = models.BooleanField(default=False)
    meta = JSONField()
