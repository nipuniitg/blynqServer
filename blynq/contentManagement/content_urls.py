__author__ = 'PRASANTH'
from django.conf.urls import url
from contentManagement import views

urlpatterns = [
     url(r'^$', views.index, name='content_index'),
     url(r'^getContent$', views.getContentJson, name='content_json'),
     url(r'^getUserContent/$', views.get_user_content, name = 'user_content_json'),
     url(r'^getUserContent/(?P<group_id>\d+)', views.get_user_content, name = 'user_content_json'),
     url(r'^uploadContent$', views.upload_content, name='upload_content'),
     url(r'^deleteItem', views.deleteItem, name='delete_item'),
     url(r'^deleteFolder', views.deleteFolder, name='delete_folder'),
     url(r'^getFoldersJson/(?P<folder_id>-?\d+)', views.get_folders_json, name='get_folders_json'),
     url(r'^getFilesJson/(?P<folder_id>-?\d+)', views.get_files_json, name='get_files_json'),
]