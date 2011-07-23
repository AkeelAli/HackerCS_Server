from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from videos.models import Faq


def home(request):
	return HttpResponseRedirect("videos/")

def faq(request):	
	if ('pk' in request.GET) and request.GET['pk'].strip():
		key=int(request.GET['pk'])
		j=1
			
	faq_list=Faq.objects.all().order_by('faq_order')
	return render_to_response('faq.html',locals())
