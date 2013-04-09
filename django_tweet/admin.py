from django.contrib import admin
import logging
from .models import TwitterAccount

log = logging.getLogger(__name__)

class TwitterAccountAdmin(admin.ModelAdmin):
    list_display = ( 'screen_name',)
    
    # def add_view(self, request, form_url='', extra_context=None):
    #     log.debug("request: %s", request)
    #     log.debug("form_url: %s", form_url)
    #     log.debug("extra_context: %s", extra_context)
    #     return begin_auth(request)


admin.site.register(TwitterAccount, TwitterAccountAdmin)
