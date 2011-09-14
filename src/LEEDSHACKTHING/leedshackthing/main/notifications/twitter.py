import tweepy
from django.conf import settings

class Twitter(object):
    
    def post(self, recipient, message):
        
        auth = tweepy.OAuthHandler(settings.OAUTH_CONSUMER_KEY, settings.OAUTH_CONSUMER_SECRET)
        auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
        
        api = tweepy.API(auth)
        
        text = "@%(recipient)s %(message)s" % {'recipient': recipient, 'message': message}
        
        api.update_status(text)