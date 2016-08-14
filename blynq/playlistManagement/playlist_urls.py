__author__ = 'PRASANTH'
from django.conf.urls import url
from playlistManagement import views

urlpatterns = [
    url(r'^$', views.index, name='playlist_index'),
    url(r'^getPlaylists', views.get_user_playlists, name='get_playlists'),
    url(r'^getFilesRecursively/(?P<parent_folder_id>-?\d+)', views.get_files_recursively_json,
        name='get_files_recursively'),
    url(r'^upsertPlaylist', views.upsert_playlist, name='upsert_playlist'),
    url(r'^deletePlaylist', views.delete_playlist, name='delete_playlist'),
    url(r'^getWidgetPlaylists', views.get_widget_playlists, name='get_widget_playlists')
]