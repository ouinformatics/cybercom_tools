from django.conf.urls.defaults import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # login
    url(r'^login/$','auth.account.views.login',{'template_name': 'registration/login.html'}),#name='login'),
    #url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
    url(r'^profile/$','auth.account.views.profile',name='profile'),
    url(r'^userdata/$','auth.account.views.userdata',name='udata'),
    url(r'^userdata_cp/$','auth.account.views.cherrypy_userdata',name='cpyudata'),
    #url(r'^testuser/$','auth.account.views.testuser',name='tdata'),
    #url(r'^logout/$','django.contrib.auth.views.logout_then_login'),# {'template_name': 'registration/logout.html'}),#
    url(r'^logout/$','auth.account.views.logout_view', name='logout'),
    url(r'^login/createnewuser/$', 'auth.account.views.new_user',name='new_user'),
    # Examples:
    # url(r'^$', 'auth.views.home', name='home'),
    # url(r'^auth/', include('auth.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
