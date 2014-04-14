from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ifmad.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^/', 'ifmad.views.login.index', name="index"),
    url(r'^updata/', include('updata.urls', namespace="updata")),
    url(r'^login/', include('login.urls', namespace="login")),
    url(r'^admin/', include(admin.site.urls)),


)
