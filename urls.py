from django.conf.urls.defaults import patterns, include, handler404, handler500
from django.conf.urls.defaults import url
from django.conf import settings

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/?$', 'views.index', name='index'),
    
    url(r'^tail/data/(?P<tail_id>\d+)/$', 'tail.views.data', name='tail_data'),
    url(r'^tail/(?P<tail_id>\d+)/$', 'tail.views.tail', name='tail_tail'),
    
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^media/(?P<path>.*)$', 'serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )