#! /usr/bin/env python
# encoding: utf-8

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
