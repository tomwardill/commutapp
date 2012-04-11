from datetime import datetime

from django.test import TestCase
from django.contrib.gis.geos import Point

from .models import UnplannedEvent

class UnplannedEventTests(TestCase):
    """ Simple tests to check that we can create and save an unplanned event """
    
    def test_deletion(self):
        to_delete = UnplannedEvent()
        to_delete.description = "test_deletion unplanned event"
        to_delete.location = Point(1.0, -1.0)
        to_delete.small_description = "test_deletion"
        to_delete.impact = "minor"
        
        to_delete.start_time = datetime.now()
        to_delete.end_time = datetime.now() 
        
        to_delete.save()
        
        # now test that we can delete it
        to_delete.delete()
        

    def test_creation(self):
        event = UnplannedEvent()
        event.description = "test_creation unplanned event"
        event.location = Point(1.0, -1.0)
        event.small_description = "test_creation"
        event.impact = "minor"
        
        event.start_time = datetime.now()
        event.end_time = datetime.now()
        
        event.save()
        
    def test_retrieval(self):
        
        event = UnplannedEvent()
        event.description = "test_retrieval unplanned event"
        event.location = Point(1.0, -1.0)
        event.small_description = "test_retrieval"
        event.impact = "minor"
        
        event.start_time = datetime.now()
        event.end_time = datetime.now()
        
        event.save()
        
        # retrieve it from the database
        retrieved = UnplannedEvent.objects.get(id = event.id)
        self.assertEqual(retrieved.description, event.description)
        
    
        
    
