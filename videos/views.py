from django.shortcuts import render_to_response
from videos.models import Stream, Video, Association, Module
from django.http import Http404

#send info about request object to template so it can use csrf token
from django.template import RequestContext

def detail(request,video_id):
	try:
		video=False
		videos=Video.objects.all()
		for v in videos:
			if (v.url_friendly()==video_id):
				video=v
				break
				
		if (not video):
			raise Http404
	except Video.DoesNotExist:
		raise Http404
	
	back=video.module_id.association_set.all()[0].association_stream_id.pk
	
	next_video=False
	
	if (video.module_id.video_count>video.video_part):
		try:
			next_video=Video.objects.get(module_id=video.module_id,video_part=(video.video_part)+1).url_friendly()
		except Video.DoesNotExist:
			pass
	if not next_video:
		stream_module=video.next_video_in_stream()
		if (stream_module):
			next_association=Association.objects.filter(association_stream_id=stream_module[0],association_part=stream_module[1])[0]
			next_video=next_association.association_module_id.video_set.all()[0].url_friendly()
				
	if (video.video_part>1):
		try:
			previous_video=Video.objects.get(module_id=video.module_id, video_part=(video.video_part)-1).url_friendly()
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

def top(request):
	entries=[]
	
	for module in Module.objects.all():
		if (module.module_rating):
			#score=float(module.module_rating)*int(module.module_raters)*len(module.video_set.all())/(int(module.module_views))
			score=float(module.module_rating)*int(module.module_raters)
			entries.append((module,score))
	
	if (entries):
		from operator import itemgetter
		entries=sorted(entries,key=itemgetter(1), reverse=True)
		
	modules=[]	
	for module_tuple in entries:
		modules.append(module_tuple[0])
	
	modules=modules[:10]
	
	return render_to_response('videos/top.html', { 'modules': modules }, context_instance=RequestContext(request))
	
def popular(request):
	entries=[]
	
	for module in Module.objects.all():
		views=int(module.module_views)
		entries.append((module,views))
	
	if (entries):
		from operator import itemgetter
		entries=sorted(entries,key=itemgetter(1), reverse=True)
		
	modules=[]	
	for module_tuple in entries:
		modules.append(module_tuple[0])
	
	modules=modules[:10]
	
	return render_to_response('videos/popular.html', { 'modules': modules }, context_instance=RequestContext(request))

def new(request):
	entries=[]
	
	for module in Module.objects.all():
		published=module.module_published
		entries.append((module,published))
	
	if (entries):
		from operator import itemgetter
		entries=sorted(entries,key=itemgetter(1), reverse=True)
		
	modules=[]	
	for module_tuple in entries:
		modules.append(module_tuple[0])
	
	modules=modules[:10]
	
	return render_to_response('videos/new.html', { 'modules': modules }, context_instance=RequestContext(request))
