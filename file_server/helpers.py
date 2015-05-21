#! /usr/bin/env python
# encoding: utf-8

import os
import re
from django.conf import settings

if settings.DEBUG:
    ROOT = os.path.join(settings.BASE_DIR, 'files', 'files')
else:
    ROOT = os.path.join(settings.STATIC_ROOT, 'files')


def human_sortable_key(old_key):
    """Create key for sorting like a human."""
    new_key = []
    for part in re.split('([0-9]+)', old_key):
        try:
            new_key.append(int(part))
        except:
            new_key.append(part)
    return new_key


def find_file_template(requested_dir):
    """Locate template for file presentation based on a given path."""
    current_dir = filter(None, requested_dir.split('/'))
    if not current_dir:
        current_dir = ['.']

    for i in range(len(current_dir)):
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

    return None
