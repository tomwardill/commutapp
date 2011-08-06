import urllib2
import base64
from StringIO import StringIO
import gzip

from models import CurrentRoad
from django.conf import settings

def _download_data(url):
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

def update_current_road():
    
    xml = _download_data(settings.DATA_URLS['currentroad'])