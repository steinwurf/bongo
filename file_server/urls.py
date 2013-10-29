from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^/(?P<current_dir>.+)$'   , 'file_server.views.show', name='show'),
    url(r'^$'                     , 'file_server.views.show', name='show'),
)