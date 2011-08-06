from django.contrib.gis.db import models
from django.contrib.auth.models import User

# Create your models here.

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
    location = models.PointField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    objects = models.GeoManager()

    
class Commute(models.Model):
    
    user = models.ForeignKey(User)
    name = models.CharField(max_length = 200)
    
    box = models.PolygonField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    