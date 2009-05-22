from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings
from inboxtix.newsletter.forms import SignupForm

from django.contrib import admin
admin.autodiscover()

context = {
    'MEDIA_URL': settings.MEDIA_URL,
    'form': SignupForm()
}

urlpatterns = patterns('',
    (r'^admin/', include('admin.site.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^get_categories/$', 'inboxtix.home.views.autocomplete_category'),
    (r'^$', direct_to_template,
        {'template': 'home/index.html', 'extra_context': context}),
    # Temporary media URL (not for production use!)
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/tom/workspace/inboxtix/media'}),
    (r'^newsletter', include('inboxtix.newsletter.urls')),    
)
