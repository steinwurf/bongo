from fabric.api import local

def start_bongo():
    local('python manage.py runserver 8080')