from django.conf.urls.defaults import *

urlpatterns = patterns('inboxtix.newsletter.views',
    (r'signup/$', 'signup'),
    (r'verify/(.+)/([\w]{32})/$', 'verify'),
)

