from django.conf.urls import url
from reports import views

urlpatterns = [
    url(r'^screen', views.screen_reports, name='screen_reports'),
    url(r'^media', views.media_reports, name='media_reports'),
    url(r'^playlist', views.playlist_reports, name='playlist_reports'),
    url(r'^generate/(?P<organization_name>\w)/$', views.refresh_report, name='refresh_report'),
]
