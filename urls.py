from django.conf.urls.defaults import patterns, include, handler404, handler500

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
)
