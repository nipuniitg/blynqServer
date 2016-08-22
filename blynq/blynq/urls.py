from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from authentication import authentication_urls
from authentication import views as auth_views
from layoutManagement import layout_urls
from playerManagement import player_urls
from reports import report_urls
from screenManagement import screen_urls
from playlistManagement import playlist_urls
from contentManagement import content_urls
from scheduleManagement import schedule_urls

urlpatterns = [
    url(r'^$', auth_views.divertToLandingPage, name='landing_page')
    , url(r'^/$', auth_views.divert_to_index_page, name='index_page')
    , url(r'^authentication/', include(authentication_urls))
    , url(r'^api/requestQuote', auth_views.request_quote, name='request_quote')
    , url(r'^api/player/', include(player_urls))
    , url(r'^api/login', auth_views.login, name='login')
    , url(r'^api/schedule/', include(schedule_urls))
    , url(r'^api/screen/', include(screen_urls))
    , url(r'^api/layout/', include(layout_urls))
    , url(r'^api/content/', include(content_urls))
    , url(r'^api/playlist/', include(playlist_urls))
    , url(r'^api/reports/', include(report_urls))
    , url(r'^admin', include(admin.site.urls))
    , url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, })
    , url(r'^.*', auth_views.divert_to_index_page)
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
