from django.shortcuts import render_to_response
from videos.models import Stream, Video, Association, Module, UserProfile
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

#send info about request object to template so it can use csrf token
from django.template import RequestContext

def index(request):
	streams_list=Stream.objects.all()
	user=request.user
	return render_to_response('videos/index.html',locals())
	
def detail(request,video_url_friendly):
	try:
		video=False
		videos=Video.objects.all()
		for v in videos:
			if (v.url_friendly()==video_url_friendly):
				video=v
				break
				
		if (not video):
			raise Http404
	except Video.DoesNotExist:
		raise Http404
	
	#marking
	videos_completed=[]
	video_completed=False
	if request.user.is_authenticated():
		videos_completed=request.user.userprofile_set.all()[0].completed_videos.all()
		if (video in videos_completed):
			video_completed=True
	
	
	back=video.module_id.association_set.all()[0].association_stream_id.url_friendly()
	
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
		if (module.module_views):
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

def random(request):
	from django.http import HttpResponseRedirect
	video=Video.objects.filter(video_part=1).order_by('?')[0]
	url="/videos/"+video.url_friendly()
	return HttpResponseRedirect(url)
	
@login_required
def mark(request,video_pk=None):
	if request.user.is_authenticated():
		profile=request.user.userprofile_set.all()[0]
		action_type=""
		pk_to_mark=""
		url=""
		
		if (not video_pk is None and video_pk!=''):
			url=Video.objects.get(pk=int(video_pk)).url_friendly()+"#interact_anchor"
		
		#mac mai
		if ('action_type' in request.POST) and request.POST['action_type'].strip():
			action_type = request.POST['action_type']

		if ('video' in request.POST) and request.POST['video'].strip():
			pk_to_mark = request.POST['video']
		
		if (action_type!="" and pk_to_mark!=""):
			video=Video.objects.get(pk=int(pk_to_mark))
			url=video.url_friendly()
			if (action_type=="mac"):
				profile.completed_videos.add(video)
			if (action_type=="mai"):
				profile.completed_videos.remove(video)
		return HttpResponseRedirect("/videos/"+url)
	
	else:
	# Do something for anonymous users.
		pass