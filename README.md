django-tweet
=============

Collect keys and blast at once



### Twitter
For each Twitter Search you add in, the app will try each time to start at now, and move back in time until... 
- it finds a tweet that it has in the DB
- it finds a tweet that has a timestamp that is further back in time than the search terms 'search until'
- twitters maximum number of api requests have been hit
