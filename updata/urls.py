from django.conf.urls import patterns, url

from updata import views






urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^upload/$', views.upload, name='upload'),
	#url(r'^getexperiments/$', views.ExperimentJSONView.as_view(), name='experiments'),
	url(r'^getexperiments/$', views.getExperiments, name='getExperiments'),
	url(r'^logout_view/$', views.logout_view, name='logout_view'),
	url(r'^process/$', views.process, name='process'),
	url(r'^consolelog/$', views.consolelog, name='consolelog'),
)
