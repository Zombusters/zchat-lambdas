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
