__author__ = 'PRASANTH'
from django.conf.urls import url
from contentManagement import views

urlpatterns = [
     url(r'^$', views.index, name='content_index'),
     url(r'^uploadContent', views.upload_content, name='upload_content'),
     url(r'^deleteContent/(?P<content_id>\d+)', views.delete_content, name='delete_item'),
     url(r'^getFoldersJson/(?P<parent_folder_id>-?\d+)', views.get_folders_json, name='get_folders_json'),
     url(r'^getFilesJson/(?P<parent_folder_id>-?\d+)', views.get_files_json, name='get_files_json'),
     url(r'^createFolder', views.create_folder, name='create_folder'),
]