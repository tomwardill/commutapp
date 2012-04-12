from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class AffectedCommute(object):
    
    def __init__(self, commute, affector):
        self.commute = commute
        self.affector = affector

class Incident(models.Model):
    
    description = models.TextField()
    location = models.PointField()

    objects = models.GeoManager()
    
class CurrentRoadWorks(models.Model):
    
    description = models.TextField()
    location = models.PointField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    objects = models.GeoManager()

class FutureRoadWorks(models.Model):
    
    description = models.TextField()
    location = models.PointField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    objects = models.GeoManager()
    
class UnplannedEvent(models.Model):
    
    description = models.TextField()
    small_description = models.TextField()
    impact = models.TextField()
    location = models.PointField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    updated = models.BooleanField()
    
    objects = models.GeoManager()


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    phonenum = models.CharField(max_length=12, blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    growlkey = models.CharField(max_length =41, blank=True)

class CommuteChoice(models.Model):
    description = models.CharField(max_length = 9)
    
    def __unicode__(self):
        return self.description
    
class Commute(models.Model):
    
    user = models.ForeignKey(User)
    name = models.CharField(max_length = 200)
    
    box = models.PolygonField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    day_choices = models.ManyToManyField(CommuteChoice)
    
    def __unicode__(self):
        return self.name
    
    
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
