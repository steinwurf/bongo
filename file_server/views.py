from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
# Create your views here.
import os

def show(request):
    path = os.path.join(settings.FILE_DIR, 'files')
    dirs = []
    files = []
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            dirs.append(item)
        else:
            files.append(item)

    return render_to_response('file_server/show.html', {
            'dirs' : dirs,
            'files': files
        }, context_instance=RequestContext(request))