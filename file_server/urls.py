from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^/(?P<requested_dir>.+)$'   , 'file_server.views.show', name='show'),
    url(r'^$'                     , 'file_server.views.show', name='show'),
)