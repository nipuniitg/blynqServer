__author__ = 'PRASANTH'
from django.conf.urls import url
from screenManagement import views

urlpatterns = [
    url(r'^$', views.screen_index, name = 'screen_index'),
    url(r'^group', views.group_index, name = 'group_index'),
    url(r'^getScreens', views.get_screens_json, name = 'screens_json'),
    url(r'^getGroups', views.get_groups_json, name='groups_json'),
    url(r'^upsertScreen', views.upsert_screen, name='upsert_screen'),
    url(r'^upsertGroup', views.upsert_group, name='upsert_group'),
    url(r'^deleteGroup', views.delete_group, name='delete_group'),
    url(r'^getCityOptionsJson', views.get_city_options, name='city_options')
]