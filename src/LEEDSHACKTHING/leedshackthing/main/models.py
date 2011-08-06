from django.contrib.gis.db import models

# Create your models here.

class Incident(models.Model):
    
    description = models.TextField()
    location = models.PointField()

    objects = models.GeoManager()
    
    
class CurrentRoad(models.Model):
    
    update_time = models.DateTimeField()