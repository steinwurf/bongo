from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader

def index(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html', {}, context_instance=RequestContext(request))