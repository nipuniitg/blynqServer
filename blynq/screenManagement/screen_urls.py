__author__ = 'PRASANTH'
from django.conf.urls import url
from screenManagement import views

urlpatterns = [
    url(r'^$', views.screen_index, name = 'screen_index'),
    url(r'^group', views.group_index, name = 'group_index'),
    url(r'^test', views.testScreen, name = 'test'),
    url(r'^getscreens', views.getScreensJson, name = 'screens_json'),
    url(r'^getGroupsJson', views.getGroupsJson, name='groups_json'),
    url(r'^addScreen$', views.add_screen, name='add_screen'),
    url(r'^addLocation$', views.add_screen_location, name='add_screen_location'),
    url(r'^addScreenSpecs$', views.add_screen_specs, name='add_screen_specs'),
    url(r'^addGroup$', views.add_group, name='add_group'),
]