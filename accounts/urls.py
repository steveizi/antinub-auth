from django.conf.urls import patterns, url
from accounts.forms import LoginForm

urlpatterns = patterns('',
    url(r'^$', 'accounts.views.profile'),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'accounts/login.djhtml',
            'authentication_form': LoginForm,
        },
        name = 'login'),
    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {
            'next_page': 'home',
        },
        name='logout'),
    url(r'^register/$', 'accounts.views.register', name='register'),
    url(r'^activate/$', 'accounts.views.activate', name='activate'),
    url(r'^profile/$', 'accounts.views.profile', name='profile'),
)