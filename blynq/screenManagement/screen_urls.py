__author__ = 'PRASANTH'
from django.conf.urls import url
from screenManagement import views

urlpatterns = [
     url(r'^$', views.screen_index, name = 'screen_index'),
     url(r'^group', views.group_index, name = 'group_index'),
     url(r'^test', views.testScreen, name = 'test'),
     url(r'^getscreens', views.getScreensJson, name = 'screens_json'),
     url(r'^getGroupsJson', views.getGroupsJson, name='groups_json')
]