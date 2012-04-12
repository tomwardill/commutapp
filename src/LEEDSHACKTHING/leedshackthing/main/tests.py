from datetime import datetime, timedelta
import os

from django.test import TestCase
from django.contrib.gis.geos import Point, Polygon
from django.contrib.auth.models import User

from .models import UnplannedEvent, Commute, CommuteChoice
from .tasks import _analyse_unplanned_data, find_affected_commutes

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
        
    
class UnplannedEventTaskTests(TestCase):
    """ Test the task of loading unplanned events from a known file """
    
    def setUp(self):
        # clean any stray events
        UnplannedEvent.objects.all().delete()
    
    def test_reading(self):
        """ Load data from our test file. The data is stale, so it passes parameter to not expire the data"""
        
        # load our test data from disk
        xml = open(os.path.join(os.path.dirname(__file__), "fixtures/unplanned.xml")).read()
        
        # False here, so we don't expire old data (as we need to test against it)
        read_situations = _analyse_unplanned_data(xml, False)
        
        # check we read the right number from the xml data
        self.assertEquals(len(read_situations), 4)
        
        # check that we saved the right number into the database
        events = UnplannedEvent.objects.all()
        
        self.assertEquals(len(events), 4)
        
    def test_stale_expiry(self):
        """ The data in our test file is old, so if you load it and expire the stale data, it should all be removed """
        
        # load our test data from disk
        xml = open(os.path.join(os.path.dirname(__file__), "fixtures/unplanned.xml")).read()
        read_situations = _analyse_unplanned_data(xml)

        # there should now be no test data
        events = UnplannedEvent.objects.all()
        self.assertEquals(len(events), 0)
               
               
class CommuteTests(TestCase):
    """ Test the commute notifications """
    
    def setUp(self):
        """ We need some events to test with """
        # first, clear any existing ones
        UnplannedEvent.objects.all().delete()
        
        event = UnplannedEvent()
        event.description = "CommuteTests unplanned event"
        event.location = Point(51.5, -0.1275)
        event.small_description = "CommuteTests"
        event.impact = "minor"
        event.updated = True
        
        event.start_time = datetime.now()
        event.end_time = datetime.now() + timedelta(hours = 1)
        
        event.save()
        
        self.event_id = event.id
        
        # we also need to clear any existing commutes
        Commute.objects.all().delete()
        
        # add the CommuteChoices we're going to need
        for x in range(7):
            cc = CommuteChoice()
            cc.description = str(x)
            cc.save()
        
        # we're also going to need a test user
        self.user = User.objects.create_user("test", "test@example.com", "test")
        self.user.save()
        
        
    def test_match_commute(self):
        """Test we can create a commute and match it to an event"""
        
        c = Commute()
        c.box = Polygon(((-100, -100), (-100, 100), (100, 100), (-100, 100), (-100, -100)))
        c.start_time = datetime.now()
        c.end_time = datetime.now() + timedelta(minutes = 5)
        c.user = self.user
        c.save()
        
        for choice in [x[0] for x in CommuteChoice.objects.values_list("id")]:
            c.day_choices.add(choice)
        c.save()
        
        # find the affected commutes
        affected = find_affected_commutes(datetime.now().time())
        self.assertEqual(len(affected), 1)
        
        # check the event has been marked as not updated
        self.assertFalse(UnplannedEvent.objects.get(id = self.event_id).updated)