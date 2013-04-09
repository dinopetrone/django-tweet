import sys
import traceback

from .services.twitter import TwitterAPI
from django.core.urlresolvers import reverse

from logging import getLogger
from django.http import HttpResponseRedirect

import settings
from .models import TwitterAccount

log = getLogger(__name__)

def begin_auth(request):
    
    twitter = TwitterAPI(
        client_key = settings.TWITTER_CONSUMER_KEY,
        client_secret = settings.TWITTER_CONSUMER_SECRET,
        callback_url = request.build_absolute_uri(reverse('django_tweet.views.save'))
    )

    try:
        auth_props = twitter.get_authentication_tokens()
    except:
        log.error(traceback.format_exc())
        log.error(traceback.format_stack())
    
    request.session['auth_props'] = auth_props
    
    return HttpResponseRedirect(auth_props['auth_url'])

def save(request,  redirect_url='/thankyou'):
    try:
        request.session['auth_props']['resource_owner_key']
    except:
        log.error('wrong domain, your auth_props are not stored in session')
        raise Exception()
    twitter = TwitterAPI(
        client_key = settings.TWITTER_CONSUMER_KEY,
        client_secret = settings.TWITTER_CONSUMER_SECRET,
        resource_owner_key = request.session['auth_props']['resource_owner_key'],
        resource_owner_secret = request.session['auth_props']['resource_owner_secret'],
        verifier=request.GET.get('oauth_verifier')
    )
    authorized_tokens = twitter.get_authorized_tokens()
    log.info("authorized_tokens: {}".format(authorized_tokens))
    

    try:
        account = TwitterAccount.objects.get(screen_name=authorized_tokens['screen_name'])
        account.update_credentials(authorized_tokens)
    except TwitterAccount.DoesNotExist:
        account_info = twitter.show_user(screen_name=authorized_tokens['screen_name'])
        TwitterAccount.create_from_obj(
            account_info, 
            oauth_token=authorized_tokens['oauth_token'], 
            oauth_token_secret=authorized_tokens['oauth_token_secret'])
        
    return HttpResponseRedirect(redirect_url)
