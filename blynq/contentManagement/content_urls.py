__author__ = 'PRASANTH'
from django.conf.urls import url
from contentManagement import views

urlpatterns = [
     url(r'^$', views.index, name='content_index'),
     url(r'^uploadContent', views.upload_content, name='upload_content'),
     url(r'^deleteContent', views.delete_content, name='delete_item'),
     url(r'^getFoldersJson/(?P<parent_folder_id>-?\d+)', views.get_folders_json, name='get_folders_json'),
     url(r'^getFilesJson/(?P<parent_folder_id>-?\d+)', views.get_files_json, name='get_files_json'),
     url(r'^createFolder', views.create_folder, name='create_folder'),
     url(r'^updateContentTitle', views.update_content_title, name='update_content_title'),
     url(r'^folderPath/(?P<current_folder_id>-?\d+)', views.folder_path, name='folder_path'),
     url(r'^moveContent', views.move_content, name='move_content'),
     url(r'^upsertUrl', views.upsert_url, name='upsert_url'),
     url(r'^validContentTypes', views.get_valid_content_types, name='valid_content_types'),
     url(r'^getWidgets', views.get_widgets, name='get_widgets'),
     url(r'^upsertWidget', views.upsert_widget, name='upsert_widget'),
     url(r'^deleteWidget', views.delete_widget, name='delete_widget'),
     url(r'^upsertFbWidget', views.upsert_fb_widget, name='upsert_fb_widget'),
     url(r'^getFbWidget/(?P<content_id>\d+)', views.getFBWidget, name='get_name_widget'),
     url(r'^checkFbPageExists', views.check_fb_page_exists, name="check_fb_page_exists"),
]