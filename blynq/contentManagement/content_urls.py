__author__ = 'PRASANTH'
from django.conf.urls import url
from contentManagement import views

urlpatterns = [
     url(r'^$', views.index, name='content_index'),
     url(r'^getContentJson$', views.getContentJson, name='content_json'),
     url(r'^uploadContent$', views.upload_content, name='upload_content'),
     url(r'^deleteItem', views.deleteItem, name='delete_item'),
     url(r'^deleteFolder', views.deleteFolder, name='delete_folder')

]