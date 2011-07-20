from django.shortcuts import render_to_response
from videos.models import Stream, Video, Association, Module
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
	except Video.DoesNotExist:
		raise Http404
	
	back=video.module_id.association_set.all()[0].association_stream_id.pk
	
	next_video=False
	
	if (video.module_id.video_count>video.video_part):
		try:
			next_video=Video.objects.get(module_id=video.module_id,video_part=(video.video_part)+1).pk
		except Video.DoesNotExist:
			pass
	if not next_video:
		stream_module=video.next_video_in_stream()
		if (stream_module):
			next_association=Association.objects.filter(association_stream_id=stream_module[0],association_part=stream_module[1])[0]
			next_video=next_association.association_module_id.video_set.all()[0].pk
				
	if (video.video_part>1):
		try:
			previous_video=Video.objects.get(module_id=video.module_id, video_part=(video.video_part)-1).pk
		except Video.DoesNotExist:	
			pass

	return render_to_response('videos/detail.html',locals(), context_instance=RequestContext(request))

def search(request):
	from helpers import get_query
	
	query_string = ''
	found_entries = None
	if ('q' in request.GET) and request.GET['q'].strip():
		query_string = request.GET['q']
		entry_query = get_query(query_string, ['module_title', 'module_description',])
        
	
	found_entries = Module.objects.filter(entry_query)
	
	return render_to_response('videos/search_results.html', { 'query_string': query_string, 'found_entries': found_entries }, context_instance=RequestContext(request))
