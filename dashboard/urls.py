from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^profile/$', 'dashboard.views.profile', name='profile'),
    url(r'^apikeys/$', 'dashboard.views.apikeys', name='apikeys'),
)