__author__ = 'PRASANTH'
from django.conf.urls import url
from playlistManagement import views

urlpatterns = [
    url(r'^$', views.index, name='playlist_index'),
    url(r'^getPlaylists', views.get_playlists, name='get_playlists'),
    url(r'^upsertPlaylist$', views.upsert_playlist, name='upsert_playlist'),
    url(r'^upsertPlaylistItems', views.upsert_playlist_items, name='upsert_playlist_items'),
    url(r'^deletePlaylist', views.delete_playlist, name='delete_playlist')
]