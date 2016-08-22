from django.conf.urls import url
from reports import views

urlpatterns = [
    url(r'^screen', views.screen_reports, name='screen_reports'),
    url(r'^media', views.media_reports, name='media_reports'),
    url(r'^playlist', views.playlist_reports, name='playlist_reports'),
]
