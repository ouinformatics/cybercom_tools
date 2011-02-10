from testproject.views import *
from testproject.floras import views
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    ('^hello/$', hello),
	('^$', myhome),
	('^cdate/$', current_datetime),
	(r'^time/plus/(\d{1,2})/$', hours_ahead),
	(r'^search-form/$', views.search_form),
	(r'^search/$', views.search),
    # Example:
    # (r'^testproject/', include('testproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
