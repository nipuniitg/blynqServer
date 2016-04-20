__author__ = 'PRASANTH'
from django.conf.urls import url
from screenManagement import views

urlpatterns = [
    url(r'^$', views.screen_index, name = 'screen_index'),
    url(r'^group', views.group_index, name = 'group_index'),
    url(r'^test', views.testScreen, name = 'test'),
    url(r'^getScreens/$', views.get_screens_json, name = 'screens_json'),
    # url(r'^getScreens/(?P<group_id>\d+)', views.get_screens_json, name = 'screens_json'),
    # url(r'^getScreen/(?P<screen_id>\d+)', views.get_screen, name = 'get_screen'),
    url(r'^getGroups', views.get_groups_json, name='groups_json'),
    url(r'^upsertScreen', views.upsertScreen, name='upsert_screen'),
    url(r'^addLocation$', views.add_screen_location, name='add_screen_location'),
    url(r'^addScreenSpecs$', views.add_screen_specs, name='add_screen_specs'),
    url(r'^addGroup$', views.add_group, name='add_group'),
    url(r'getSelectableScreens/', views.get_selectable_screens_json, name='selectable_screens_json'),
    url(r'getSelectableGroups/', views.get_selectable_groups_json, name='selectable_groups_json'),
]