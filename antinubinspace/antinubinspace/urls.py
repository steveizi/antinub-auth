from django.conf.urls import patterns, include, url
from django.contrib import admin

from aniauth.forms import LoginForm

urlpatterns = patterns('',
    # Admin urls
    url(r'^admin/', include(admin.site.urls)),
    
    # Index
    url(r'^$', 'aniauth.views.register', name='home'),
    ### url(r'^$', 'portal.views.index', name='index'),
    
    # Auth
    url(r'^account/$', 'aniauth.views.account', name='account'),
    url(
        r'^account/login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'login.djhtml',
            'authentication_form': LoginForm,
        },
         name='login'),
    url(r'^account/logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': 'home'},
        name='logout'),
    
    url(r'^account/register/$', 'aniauth.views.register', name='register'),
    url(r'^account/profile/$', 'aniauth.views.profile', name='profile'),
)
