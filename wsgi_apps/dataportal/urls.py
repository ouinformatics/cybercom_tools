from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^getempty/','dataportal.editCat.views.empty_Load', name='empty_Load'),
    # Example:
    # (r'^example/', include('example.foo.urls')),
#    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'editCat/login.html'}),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', 'dataportal.editCat.views.main_commons', name='commons'),
    url(r'^catalog/','dataportal.editCat.views.catalog', name='catalog'),
    url(r'^commons/','dataportal.editCat.views.main_catalog', name='commons'),
    url(r'^common/','dataportal.editCat.views.load_common', name='commons'),
    url(r'^event/','dataportal.editCat.views.load_event', name='events'),
# Ajax Calls
    url(r'^getcommon/','dataportal.editCat.views.ajax_com', name='ajax_com'),
    url(r'^delcommon/','dataportal.editCat.views.ajax_com_del', name='ajax_com_del'),
    url(r'^getcatalog/','dataportal.editCat.views.ajax_cat', name='ajax_cat'),
    url(r'^delcatalog/','dataportal.editCat.views.ajax_cat_del', name='ajax_cat_del'),
    url(r'^getevent/','dataportal.editCat.views.ajax_event', name='ajax_event'),
    url(r'^delevent/','dataportal.editCat.views.ajax_event_del', name='ajax_event_del'),
    url(r'^getresult/','dataportal.editCat.views.ajax_result', name='ajax_result'),
    url(r'^delresult/','dataportal.editCat.views.ajax_result_del', name='ajax_result_del'),
    url(r'^getlocation/','dataportal.editCat.views.ajax_loc', name='ajax_loc'),
    url(r'^getmethod/','dataportal.editCat.views.ajax_meth', name='ajax_meth'),
    url(r'^gettype/','dataportal.editCat.views.ajax_type', name='ajax_type'),
# login
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
# Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
    #('^$', 'rpc4django.views.serve_rpc_request'),
    ('^RPC2/$', 'rpc4django.views.serve_rpc_request'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
