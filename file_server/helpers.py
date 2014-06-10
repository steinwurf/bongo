import os
import re
from django.conf import settings

if settings.DEBUG:
    ROOT = os.path.join(settings.BASE_DIR, 'files', 'files')
else:
    ROOT = os.path.join(settings.STATIC_ROOT, 'files')


def tryparse(value):
    try:
        return int(value)
    except:
        return value


def get_human_sortable_key_func(func):
    return lambda key: \
        [tryparse(parts) for parts in re.split('([0-9]+)', func(key))]


def sort_humanly(list, func=lambda key: key):
    list.sort(key=get_human_sortable_key_func(func))


def find_file_template(requested_dir):
    current_dir = filter(None, requested_dir.split('/'))
    depth = len(current_dir)
    for i in range(depth):
        path = os.path.join(ROOT, *current_dir)
        try:
            for item in os.listdir(path):
                if os.path.isdir(os.path.join(path, item)) \
                   or not item.endswith('.bongo'):
                    continue
                else:
                    current_dir.append(item)
                    return os.path.join('files', *current_dir)
        except Exception, e:
            print(e)
            continue
        current_dir.remove(current_dir[-1])
    default_bongo_file = os.path.join(
        settings.TEMPLATE_DIRS[-1], 'default.bongo')
    if os.path.exists(default_bongo_file):
        return 'default.bongo'
    else:
        return None
