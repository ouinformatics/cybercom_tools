from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^getempty/','datacatalog.editCat.views.empty_Load', name='empty_Load'),
    # Example:
    # (r'^example/', include('example.foo.urls')),
#    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'editCat/login.html'}),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #url(r'', 'datacatalog.editCat.views.main_commons', name='commons'),
    url(r'^$', 'datacatalog.editCat.views.main_commons', name='commons'),
    url(r'^catalog/','datacatalog.editCat.views.catalog', name='catalog'),
    url(r'^commons/','datacatalog.editCat.views.main_catalog', name='commons'),
    url(r'^common/','datacatalog.editCat.views.load_common', name='commons'),
    url(r'^event/','datacatalog.editCat.views.load_event', name='events'),
# Ajax Calls
    url(r'^getcommon/','datacatalog.editCat.views.ajax_com', name='ajax_com'),
    url(r'^delcommon/','datacatalog.editCat.views.ajax_com_del', name='ajax_com_del'),
    url(r'^getcatalog/','datacatalog.editCat.views.ajax_cat', name='ajax_cat'),
    url(r'^delcatalog/','datacatalog.editCat.views.ajax_cat_del', name='ajax_cat_del'),
    url(r'^getevent/','datacatalog.editCat.views.ajax_event', name='ajax_event'),
    url(r'^delevent/','datacatalog.editCat.views.ajax_event_del', name='ajax_event_del'),
    url(r'^getresult/','datacatalog.editCat.views.ajax_result', name='ajax_result'),
    url(r'^delresult/','datacatalog.editCat.views.ajax_result_del', name='ajax_result_del'),
    url(r'^getlocation/','datacatalog.editCat.views.ajax_loc', name='ajax_loc'),
    url(r'^getmethod/','datacatalog.editCat.views.ajax_meth', name='ajax_meth'),
    url(r'^getmethPar/','datacatalog.editCat.views.ajax_methPar', name='ajax_methPar'),
    url(r'^gettype/','datacatalog.editCat.views.ajax_type', name='ajax_type'),
    url(r'^getvar/','datacatalog.editCat.views.ajax_var', name='ajax_var'),
    url(r'^getws_view/','datacatalog.editCat.views.webservice_view', name='ajax_ws_view'),
    url(r'^getempty/','datacatalog.editCat.views.empty_Load', name='empty_Load'),
#webservice_view
# login
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
    #url(r'^accounts/logout/accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
    #url(r'^accounts/logout/$','datacatalog.editCat.views.logout_view', name='logout'),
    #url(r'^accounts/login/createnewuser/$', 'datacatalog.editCat.views.new_user',name='new_user'),
# Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
    #('^$', 'rpc4django.views.serve_rpc_request'),
    ('^RPC/$', 'rpc4django.views.serve_rpc_request'),
    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
