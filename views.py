from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from videos.models import Faq, Stream
from django.http import Http404

from django.template import RequestContext

def home(request):
	streams_list=Stream.objects.all()
	return render_to_response('videos/index.html',locals())

def stream_detail(request,stream_url_friendly):
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

def GetAuthSubUrl():
	next = 'http://www.example.com/video_upload.pyc'
	scope = 'http://gdata.youtube.com'
	secure = False
	session = True

def login(request):
	import gdata.youtube
	import gdata.youtube.service
	yt_service = gdata.youtube.service.YouTubeService()
	yt_service.ssl = True
	yt_service.developer_key = 'AI39si4w3shgHsc41LIYau0qP_aUnIVaPs5Q5Claz1w2VMrMh9p14QR1Ww'
	yt_service = gdata.youtube.service.YouTubeService()
	authSubUrl=yt_service.GenerateAuthSubURL('http://hackercs.com', 'http://gdata.youtube.com', secure=False, session=True)
	return render_to_response('login.html',{ 'authSubUrl': authSubUrl})
	
