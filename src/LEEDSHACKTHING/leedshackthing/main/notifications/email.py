from django.core.mail import send_mail

class Email(object):
    
    def post(self, recipient, message):
        
        send_mail('Commute Warning', message, 'warning@commutapp.com', [recipient])
