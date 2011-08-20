from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
#import for custom registration with profile
from forms import CustomRegistrationForm
from registration.views import register

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
	#custom registration form that creates profile
	url(r'^login/$',register,{'form_class' : CustomRegistrationForm},name='registration_register'),
		(r'^accounts/', include('registration.urls')),
		
	#django password reset
		(r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/accounts/password/reset/done/'}),
		(r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
		(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/accounts/password/done/'}),
		(r'^accounts/password/done/$', 'django.contrib.auth.views.password_reset_complete'),

	#password change
		(r'^accounts/password/change/$','django.contrib.auth.views.password_change',{'post_change_redirect' : '/accounts/password/change/done/'}),
		(r'^accounts/password/change/done/$','django.contrib.auth.views.password_change_done'),
		
		(r'^users/',include('users.urls')),
	# Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	
		(r'^streams/(?P<stream_url_friendly>[\w\-]+)/$','cs.views.stream_detail'),
)
