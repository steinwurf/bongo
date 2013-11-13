import re

def tryparse(value):
    try:
        return int(value)
    except:
        return value

def get_human_sortable_key(key):
    return [ tryparse(parts) for parts in re.split('([0-9]+)', key) ]

def sort_humanly(list):
    list.sort(key=get_human_sortable_key)