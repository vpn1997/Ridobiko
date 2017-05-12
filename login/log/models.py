from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name='profile',unique=True)
    number=models.CharField(max_length=10)

    def __unicode__(self):
        return self.user.username


