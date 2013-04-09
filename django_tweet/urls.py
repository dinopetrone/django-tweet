from django.conf.urls.defaults import include, patterns

from .views import save, begin_auth
from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    
    url(r'^begin_auth/', begin_auth, name="twitter_callback"),
    url(r'^save/', save, name="twitter_callback"),
)

