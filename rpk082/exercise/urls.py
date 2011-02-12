from django.conf.urls.defaults import *

urlpatterns = patterns('',
   	(r'^$', 'rpk082.exercise.views.home_page'),
  	(r'^login/', 'rpk082.exercise.views.login'),
  	(r'^add/', 'rpk082.exercise.views.add'),
  	(r'^logout/', 'rpk082.exercise.views.logout'),
  	(r'^all/', 'rpk082.exercise.views.all_users'),
  	(r'^remove/', 'rpk082.exercise.views.remove'),
  	
#	(r'^index/', 'rpk082.robot.views.index'), #TODO remove this when it'll be replaced with good xhr
#	(r'^xhr/', include('rpk082.robot.urls')),
#	(r'^statuses/', include('rpk082.robot.urls')),

)
