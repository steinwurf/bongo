from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
# Create your views here.
import os

def show(request, current_dir = '/'):
    print current_dir
    path = os.path.join(
        settings.BASE_DIR if settings.DEBUG else settings.STATIC_ROOT, 'files')

    current_dir = filter(None, current_dir.split('/'))
    if current_dir:
        path = os.path.join(path, *current_dir)

    dirs = []
    files = []
    for item in os.listdir(path):
        # Don't show hidden files
        if item.startswith('.'):
            continue

        if os.path.isdir(os.path.join(path, item)):
            dirs.append(item)
        else:
            files.append(item)

    return render_to_response('file_server/show.html', {
            'dirs'      : dirs,
            'files'     : files,
            'current_dir' : current_dir,
        }, context_instance=RequestContext(request))