from django.core.exceptions import PermissionDenied
from django.core.servers.basehttp import FileWrapper
from django.http import Http404
from django.http import StreamingHttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from helpers import sort_humanly, find_file_template, ROOT
import mimetypes
import os, time

def show(request, requested_dir = '/'):
    # Get the requested directory. split the current dir with / and filter out
    # any None values.
    current_dir = filter(None, requested_dir.split('/'))
    if current_dir:
        path = os.path.join(ROOT, *current_dir)
    else:
        path = ROOT
    dirs = []
    files = []
    items = []
    try:
        items = os.listdir(path)
    except OSError, e:
        if e.errno == 2:
            raise Http404
        elif e.errno == 13:
            raise PermissionDenied
        elif e.errno == 20:
            wrapper      = FileWrapper(open(path))
            content_type = mimetypes.guess_type(path)[0]

            if not content_type:
                content_type = 'application/x-executable'

            response     = StreamingHttpResponse(wrapper,content_type=content_type)
            response['Content-Length']      = os.path.getsize(path)
            response['Content-Disposition'] = "attachment; filename={}".format(current_dir[-1])
            return response
        else:
            raise

    for item in items:
        # Don't show hidden files and templates
        if item.startswith('.') or item.endswith('.bongo'):
            continue

        if os.path.isdir(os.path.join(path, item)):
            dirs.append(item)
        else:
            stats = os.stat(os.path.join(path, item))
            relative_item_path = os.path.join('files', *current_dir)
            files.append({
                'filename' : item,
                'path'     : os.path.join(relative_item_path, item),
                'size'     : "{0:.2f}MB".format(stats.st_size/1024.0/1024.0),
                'time'     : time.ctime(stats.st_mtime)
            })

    # Hack to add trailing slash in template if needed
    if current_dir:
        current_dir.append('')

    sort_humanly(dirs)
    sort_humanly(files, lambda item : item['filename'])

    return render_to_response('file_server/show.html', {
            'dirs'          : dirs,
            'files'         : files,
            'current_dir'   : current_dir,
            'file_template' : find_file_template(requested_dir)
        }, context_instance=RequestContext(request))