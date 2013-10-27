from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^', 'file_server.views.show', name='show'),
)