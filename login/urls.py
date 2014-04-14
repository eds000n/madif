from django.conf.urls import patterns, url

from login import views






urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.loginForm, name='loginForm'),
	#url(r'^$', views.loginView, name='loginView'),
#	url(r'^$',views.IndexView.as_view(),name='index'),

)
