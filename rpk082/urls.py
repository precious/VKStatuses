from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   	(r'^$', 'rpk082.robot.views.statuses'),
	(r'^index/', 'rpk082.robot.views.index'), #TODO remove this when it'll be replaced with good xhr
	(r'^xhr/', include('rpk082.robot.urls')),
	(r'^statuses/', include('rpk082.robot.urls')),
	
	(r'^exercise/', include('rpk082.exercise.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^task/$','rpk082.robot.views.task'),
)
