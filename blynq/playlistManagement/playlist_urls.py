__author__ = 'PRASANTH'
from django.conf.urls import url
from playlistManagement import views

urlpatterns = [
     url(r'^$', views.index, name='playlist_index'),
     url(r'^getPlaylistsJson', views.getPlaylistsJson, name='playlists_json')
]