from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$',          'bongo.views.index', name='index'),
    url(r'^about',      'bongo.views.about', name='about'),
    url(r'^benchmarks', include('benchmarks.urls')),
)
