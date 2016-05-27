__author__ = 'NIPUN'
from django.conf.urls import url
from scheduleManagement import views

urlpatterns = [
    url(r'^$', views.index, name='schedule_index'),
    url(r'^upsertSchedule', views.upsert_schedule, name='upsert_schedule'),
    url(r'^getScreenData', views.get_screen_data, name='screen_calendar'),
    url(r'^deviceKeyActive', views.device_key_active, name='device_key_active'),
    url(r'^addSchedule', views.add_schedule, name='add_schedule'),
    url(r'^getSchedules', views.get_schedules, name='get_schedules'),
    url(r'^deleteSchedule', views.delete_schedule, name='delete_schedule'),
    url(r'^getScreenSchedulesJson/(?P<screen_id>\d+)', views.get_screen_schedules, name='get_screen_schedules'),
    url(r'^getPlyalistSchedulesJson/(?P<playlist_id>\d+)', views.get_playlist_schedules, name='get_playlist_schedules'),
]