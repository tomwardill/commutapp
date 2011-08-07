import urllib2
import base64
from StringIO import StringIO
import gzip
from dateutil.parser import parse as date_parse
import operator
from datetime import datetime

from lxml import etree

from django.contrib.gis.geos import Point

from models import CurrentRoadWorks, FutureRoadWorks, UnplannedEvent, Commute, AffectedCommute
from django.conf import settings

import pyrowl
from leedshackthing.main.views.sms import SMS

namespaces = {'datex': 'http://datex2.eu/schema/1_0/1_0', 'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/', 'xsd': 'http://www.w3.org/2001/XMLSchema'}

def _download_data(url):
    
    if settings.LOCAL_DATA:
        request = urllib2.Request(url)
        return urllib2.urlopen(request).read()
    
    request = urllib2.Request(url)
    base64string = base64.encodestring(
        '%s:%s' % (settings.TRAFFIC_USERNAME, settings.TRAFFIC_PASSWORD)
        ).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    request.add_header('Accept-encoding', 'gzip,deflate')
    result = urllib2.urlopen(request)

    if result.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(result.read())
        f = gzip.GzipFile(fileobj = buf)
        data = f.read()
    
    return data

def _get_time(time_string):
    """ Convert the string from the xml into a datetime """
    return date_parse(time_string)

def update_current_road():
    
    xml = _download_data(settings.DATA_URLS['currentroad'])
    data = etree.fromstring(xml)
    situations = data.xpath('//datex:situationRecord', namespaces = namespaces)
    
    # remove all existing RoadWorks
    CurrentRoadWorks.objects.all().delete()
    
    for situation in situations:
        c = CurrentRoadWorks()
        c.description = situation.xpath('./datex:nonGeneralPublicComment/datex:comment/datex:value', namespaces = namespaces)[0].text
        latitude = situation.xpath('.//datex:latitude', namespaces = namespaces)[0].text
        longitude = situation.xpath('.//datex:longitude', namespaces = namespaces)[0].text
        
        c.location = Point(float(longitude), float(latitude))
        c.start_time = _get_time(situation.xpath('.//datex:overallStartTime', namespaces = namespaces)[0].text)
        c.end_time = _get_time(situation.xpath('.//datex:overallEndTime', namespaces = namespaces)[0].text)
        
        c.save()
        
    return len(situations)

def update_future_road():
    
    xml = _download_data(settings.DATA_URLS['futureroad'])
    data = etree.fromstring(xml)
    
    situations = data.xpath('//datex:situationRecord', namespaces = namespaces)
    
    # remove all existing RoadWorks
    FutureRoadWorks.objects.all().delete()
    
    for situation in situations:
        c = FutureRoadWorks()
        c.description = situation.xpath('./datex:nonGeneralPublicComment/datex:comment/datex:value', namespaces = namespaces)[0].text
        latitude = situation.xpath('.//datex:latitude', namespaces = namespaces)[0].text
        longitude = situation.xpath('.//datex:longitude', namespaces = namespaces)[0].text
        
        c.location = Point(float(longitude), float(latitude))
        c.start_time = _get_time(situation.xpath('.//datex:overallStartTime', namespaces = namespaces)[0].text)
        c.end_time = _get_time(situation.xpath('.//datex:overallEndTime', namespaces = namespaces)[0].text)
        
        c.save()
        
    return len(situations)

def update_unplanned_events():
    
    xml = _download_data(settings.DATA_URLS['unplannedevent'])
    data = etree.fromstring(xml)
    
    situations = data.xpath('//datex:situationRecord', namespaces = namespaces)
    
    # remove all existing RoadWorks
    UnplannedEvent.objects.all().delete()
    
    for situation in situations:
        c = UnplannedEvent()
        c.description = situation.xpath('./datex:nonGeneralPublicComment/datex:comment/datex:value', namespaces = namespaces)[0].text
        latitude = situation.xpath('.//datex:latitude', namespaces = namespaces)[0].text
        longitude = situation.xpath('.//datex:longitude', namespaces = namespaces)[0].text
        c.location = Point(float(longitude), float(latitude))
        
        c.small_description = situation.xpath('.//datex:descriptor', namespaces = namespaces)[0].getchildren()[0].text
        c.impact = situation.xpath('.//datex:impactOnTraffic', namespaces = namespaces)[0].text
        
        c.start_time = _get_time(situation.xpath('.//datex:overallStartTime', namespaces = namespaces)[0].text)
        c.end_time = _get_time(situation.xpath('.//datex:overallEndTime', namespaces = namespaces)[0].text)
        
        c.save()
        
    return len(situations)

def find_affected_commutes(time):
    """ Find all events that match"""
    
    in_time = Commute.objects.filter(start_time__lt = time, end_time__gt = time)
    
    affected = []
    for event in UnplannedEvent.objects.all():
        for c in in_time:
            if c.box.contains(event.location):
                a = AffectedCommute(c, event)
                affected.append(a)
    
    return affected

def notify_users():
    
    now = datetime.now().time()
    commutes = find_affected_commutes(now)
    
    for c in commutes:
        
        try:
            profile = c.commute.user.get_profile()
        except:
            continue
        if profile.growlkey:
            sendgrowl(profile.growlkey, c.affector.description)
        if profile.phonenum:
            sendSMS(profile.phonenum, "%s: %s" % (c.affector.impact, c.affector.small_description))
    

def sendgrowl(growlkey, message):
    
    growlkey = str(growlkey)
    
    p = pyrowl.Pyrowl(growlkey)
    p.push("leedshackthing", "Commute Update", message)

def sendSMS(recipent, message):
    s = SMS()
    s.post(recipent, message)
