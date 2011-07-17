from django.shortcuts import render_to_response
from videos.models import Stream, Video
from django.http import Http404

#send info about request object to template so it can use csrf token
from django.template import RequestContext

def index(request):
	streams_list=Stream.objects.all()
	return render_to_response('videos/index.html',locals())

def stream_detail(request,stream_id):
	try:
		stream=Stream.objects.get(pk=stream_id)
		associations_list=stream.association_set.all()
	except Stream.DoesNotExist:
		raise Http404
	return render_to_response('videos/stream_detail.html',locals(),context_instance=RequestContext(request))

def detail(request,video_id):
	try:
		video=Video.objects.get(pk=video_id)
		back=request.META['HTTP_REFERER']
	except Video.DoesNotExist:
		raise Http404
	return render_to_response('videos/detail.html',locals(), context_instance=RequestContext(request))


