from django.contrib.gis import admin
from leedshackthing.main.models import UnplannedEvent, Commute, UserProfile


admin.site.register(UnplannedEvent, admin.OSMGeoAdmin)
admin.site.register(Commute)
admin.site.register(UserProfile)

