from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cs.views.home', name='home'),
    # url(r'^cs/', include('cs.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
		(r'^$','cs.views.home'),	
		(r'^videos/',include('videos.urls')),
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
		(r'^faq/$','cs.views.faq'),
	# Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
