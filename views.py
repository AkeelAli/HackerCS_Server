from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from videos.models import Faq


def home(request):
	return HttpResponseRedirect("videos/")

def faq(request):
	faq_list=Faq.objects.all().order_by('faq_order')
	return render_to_response('faq.html',locals())
