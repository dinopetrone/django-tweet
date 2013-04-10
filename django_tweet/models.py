
import json
import time
import logging
from time import mktime
from datetime import datetime
from django.db import models
from django.utils.timezone import utc
from django.db.models.signals import post_save
from django.dispatch import receiver
from celery.task.control import revoke
from .tasks import send_tweet

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)




class TwitterAccount(models.Model):
    twitter_id = models.BigIntegerField()
    verified = models.BooleanField(default=False)
    profile_image_url_https = models.URLField(blank=True)
    screen_name = models.CharField(max_length=200)
    oauth_token = models.CharField(max_length=255, blank=True)
    oauth_secret = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.screen_name

    @property
    def valid(self):
        try:
            return self._valid
        except AttributeError:
            self._valid = True
            return self._valid

    @valid.setter
    def valid(self, value):
        self._valid = value

    def update_credentials(self,authorized_tokens):
        self.oauth_token = authorized_tokens['oauth_token']
        self.oauth_secret = authorized_tokens['oauth_token_secret']
        self.save()

    @staticmethod
    def create_from_obj(obj, oauth_token, oauth_token_secret):
        account = TwitterAccount()
        account.twitter_id              = obj['id']
        account.screen_name             = obj['screen_name']
        account.profile_image_url_https = obj['profile_image_url_https']
        account.verified                = obj['verified']
        account.oauth_token             = oauth_token
        account.oauth_secret            = oauth_token_secret
        account.save()
        return account

class ScheduledTweet(models.Model):
    tweet_message = models.TextField(max_length=180)
    release_date = models.DateTimeField()
    task_id = models.CharField(max_length=100, null=True, editable=False)
    
    def __unicode__(self):
        return self.tweet_message

    def save(self, *args, **kwargs):
        #if the task exists, kill it, just in case they updated the time.
        if(self.task_id):
            revoke(self.task_id)

        task = send_tweet.apply_async((self.id,))

        self.task_id = task.task_id
        super(ScheduledTweet, self).save(*args, **kwargs)