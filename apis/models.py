from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.dispatch import receiver
from django.db.models import signals
from django.conf import settings
from rest_framework.authtoken.models import Token

# @receiver(signals.post_save, sender=User)
# def generate_token(sender, instance, created, **kwargs):
#     Token.objects.create(user=instance)
#     print("Token Created")

class Images(models.Model):
    flickr_id = models.CharField(max_length=30, blank=False, null=False)
    owner = models.CharField(max_length=255, null=True, default=None)
    title = models.CharField(max_length=255, null=True, default=None)
    image = models.FileField()
    secret = models.CharField(max_length=50, null=True, default=None)
    farm = models.CharField(max_length=50, null=True, default=None)
    server = models.CharField(max_length=50, null=True, default=None)
    description = models.TextField(blank=True)
    comments_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'images'

class Group(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    flickr_id = models.CharField(max_length=30, blank=False, null=False)
    name = models.CharField(max_length=255, null = False, default=None)
    member_count = models.IntegerField(default=0)
    image_count = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'groups'


class GroupImage(models.Model):
    group = models.ForeignKey(Group,related_name="group_images",on_delete=models.CASCADE)
    image = models.ForeignKey(Images,related_name="group_images",on_delete=models.CASCADE)
    class Meta:
        db_table = 'group_images'


















