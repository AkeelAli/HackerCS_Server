from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from videos.models import Faq, Stream
from django.http import Http404
from django.contrib.auth.models import User

from django.template import RequestContext

def home(request):
	streams_list=Stream.objects.all()
	user=request.user
	return render_to_response('videos/index.html',locals())

def stream_detail(request,stream_url_friendly):
	user=request.user
	completed_videos=user.userprofile_set.all()[0].completed_videos.all()
	try:
		stream=False
		streams=Stream.objects.all()
		for s in streams:
			if (s.url_friendly()==stream_url_friendly):
				stream=s
				break
				
		if (not stream):
			raise Http404
			
		associations_list=stream.association_set.all().order_by('association_part')
	except Stream.DoesNotExist:
		raise Http404
	
	return render_to_response('videos/stream_detail.html',locals(),context_instance=RequestContext(request))
	
def faq(request):	
	if ('pk' in request.GET) and request.GET['pk'].strip():
		key=int(request.GET['pk'])
		j=1
			
	faq_list=Faq.objects.all().order_by('faq_order')
	return render_to_response('faq.html',locals())
