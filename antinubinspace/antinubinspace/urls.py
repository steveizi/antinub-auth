from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Admin urls
    url(r'^admin/', include(admin.site.urls)),
    
    # Index
    url(r'^$', 'aniauth.views.register', name='register'),
    ### url(r'^$', 'portal.views.index', name='index'),
    
    # Auth
    url(r'^account/$', 'aniauth.views.account', name='account'),
    url(r'^account/login/$', 'aniauth.views.login', name='login'),
    url(r'^account/logout/$', 'aniauth.views.logout', name='logout'),
    
    url(r'^account/register/$', 'aniauth.views.register', name='register'),
    url(r'^account/profile/$', 'aniauth.views.profile', name='register'),
)
