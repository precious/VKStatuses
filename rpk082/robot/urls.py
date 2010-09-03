from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^last(?P<records>\d+)s/$', 'rpk082.robot.views.lastrecords'),
	(r'^last(?P<record>\d+)/$', 'rpk082.robot.views.lastrecord'),
	
	(r'^last(?P<records>\d+)commented/$', 'rpk082.robot.views.last_commented'),
	
	(r'^contacts/$', 'rpk082.robot.views.contacts'),
	
	(r'^status_(?P<stat_id>\d+)/$', 'rpk082.robot.views.status'),
	(r'^send_comment/$', 'rpk082.robot.views.send_comment'),
	
	(r'^statistics/$','rpk082.robot.views.statistic_charts'),
)
