import base64
from xml.etree import ElementTree
import urllib2

class SMS(object):

    def post(self, recipient, message):

        template_values = {}
        if recipient and message:
            
            url = 'http://api.esendex.com/v1.0/messagedispatcher'
            encoded_username = base64.urlsafe_b64encode('sms9@hodgetastic.com:leedshack')
            
            xml = """<?xml version='1.0' encoding='UTF-8'?><messages><accountreference>%s</accountreference><message><to>%s</to><body>%s</body></message></messages>""" % ('EX0081171', recipient, message)  
            
            request = urllib2.Request(url, data = xml)
            request.headers = {'Content-Type' : 'text/xml', 'Authorization' : "Basic %s" % (encoded_username)}
            result = urllib2.urlopen(request)
            
            #result = urllib2.urlopen(
            #    url,
            #    data = xml, 
            #    headers={'Content-Type' : 'text/xml', 'Authorization' : "Basic %s" % (encoded_username)})
            res = result.read()

            if result.status_code == 200:
                root = ElementTree.fromstring(result.content)
                template_values['message_id'] = root.getchildren()[0].attrib['id']
                template_values['message'] = "Success!"
 
        