import mimetypes
import os
import time

from django.core.exceptions import PermissionDenied
from django.core.servers.basehttp import FileWrapper
from django.http import Http404
from django.http import StreamingHttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from helpers import human_sortable_key, find_file_template


def show(request, root, requested_dir='/'):
    """Get the requested directory."""
    # split the current dir with / and filter out any None values.
    current_dir = filter(None, requested_dir.split('/'))
    path = os.path.join(root, *current_dir)
    try:
        items = os.listdir(path)
    except OSError, e:
        if e.errno == 2:
            raise Http404
        elif e.errno == 13:
            raise PermissionDenied
        elif e.errno == 20:
            # you found a file
            return download_file(path)
        else:
            raise

    directories = []
    files = []
    for item in items:
        # Don't show hidden files and templates
        if item.startswith('.') or item.endswith('.bongo'):
            continue
        item_path = os.path.join(path, item)

        info = {
            'name': item,
            'path': os.path.join(*(current_dir + [item]))
        }

        if os.path.isdir(item_path):
            directories.append(info)
        else:
            stats = os.stat(item_path)
            info['size'] = "{0:.2f}MB".format(stats.st_size / 1024.0 / 1024.0)
            info['time'] = time.ctime(stats.st_mtime)
            files.append(info)

    directories.sort(key=lambda item: human_sortable_key(item['name']))
    files.sort(key=lambda item: human_sortable_key(item['name']))

    return render_to_response(
        template_name='file_server/show.html',
        context={
            'directories': directories,
            'files': files,
            'current_dir': current_dir,
            'file_template': find_file_template(current_dir, path)
        },
        context_instance=RequestContext(request))


def download_file(path):
    """Create a response to a request for downloading."""
    wrapper = FileWrapper(open(path))
    content_type = mimetypes.guess_type(path)[0] or 'application/x-executable'

    response = StreamingHttpResponse(wrapper,
                                     content_type=content_type)
    response['Content-Length'] = os.path.getsize(path)
    response['Content-Disposition'] =\
        "attachment; filename={}".format(os.path.basename(path))
    return response
