from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^', 'benchmarks.views.show', name='show'),
)