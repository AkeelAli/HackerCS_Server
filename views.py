from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from videos.models import Faq, Stream

from django.template import RequestContext

def home(request):
	streams_list=Stream.objects.all()
	return render_to_response('videos/index.html',locals())

def stream_detail(request,stream_id):
	try:
		stream=Stream.objects.get(pk=stream_id)
		associations_list=stream.association_set.all()
	except Stream.DoesNotExist:
		raise Http404
	return render_to_response('videos/stream_detail.html',locals(),context_instance=RequestContext(request))
	
def faq(request):	
	if ('pk' in request.GET) and request.GET['pk'].strip():
		key=int(request.GET['pk'])
		j=1
			
	faq_list=Faq.objects.all().order_by('faq_order')
	return render_to_response('faq.html',locals())
