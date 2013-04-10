import pytz
from django.utils.timezone import utc, make_naive
import celery
from .services.twitter import TwitterAPI
import settings


@celery.task(name='send-tweet')
def send_tweet(tweet_id):
    from .models import ScheduledTweet, TwitterAccount
    accounts = TwitterAccount.objects.all()
    try:
        tweet = ScheduledTweet.objects.get(id=tweet_id)
    except:
        #must have been deleted?
        return
    for account in accounts:
        twapi = TwitterAPI( 
            client_key = settings.TWITTER_CONSUMER_KEY, 
            client_secret = settings.TWITTER_CONSUMER_SECRET,
            resource_owner_key = account.oauth_token,
            resource_owner_secret = account.oauth_secret
        )
        twapi.tweet_message(tweet.tweet_message)