#! /usr/bin/env python
# encoding: utf-8

import os
import re


def human_sortable_key(old_key):
    """Create key for sorting like a human."""
    new_key = []
    for part in re.split('([0-9]+)', old_key):
        try:
            new_key.append(int(part))
        except:
            new_key.append(part)
    return new_key


def find_file_template(current_dir, path):
    """Locate template for file presentation based on a given path."""
    for sub_dir in reversed(['.'] + current_dir):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if not os.path.isdir(item_path) and item.endswith('.bongo'):
                return item_path
        path = os.path.join(path, '..')
    return None
