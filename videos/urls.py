from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('videos.views',
		url(r'^$','index'),
		url(r'^streams/(?P<stream_id>\d+)/$','stream_detail'),
		url(r'^search/$','search'),
		url(r'^top/$','top'),
		url(r'^popular/$','popular'),
		url(r'^new/$','new'),
		#the following url must be at the end (otherwise risk matching with other words)
		url(r'^(?P<video_id>[\w\-]+)/$','detail'),
)
