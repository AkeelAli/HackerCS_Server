from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('videos.views',
		url(r'^$','index'),
		url(r'^(?P<video_id>\d+)/$','detail'),
		url(r'^streams/(?P<stream_id>\d+)/$','stream_detail'),
)
