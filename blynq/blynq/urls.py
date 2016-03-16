from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from authentication import authentication_urls
from authentication import views as auth_views
from screenManagement import screen_urls
from playlistManagement import playlist_urls
from contentManagement import content_urls
from scheduleManagement import schedule_urls


urlpatterns = [
    url(r'^authentication/', include(authentication_urls)),
    url(r'^schedule/', include(schedule_urls)),
    url(r'^screen/', include(screen_urls)),
    url(r'^content/', include(content_urls)),
    url(r'^playlist/', include(playlist_urls)),
    url(r'^home/', auth_views.homePage, name='homepage'),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
   ]