__author__ = 'PRASANTH'
from django.conf.urls import url
from scheduleManagement import views

urlpatterns = [
    url(r'^$', views.index, name='schedule_index'),
    url(r'^upsertSchedule', views.upsert_schedule, name='upsert_schedule'),
    url(r'^getScreenData/screen/(?P<screen_id>\d+)/lastreceived/(?P<last_received>\d{14})', views.get_screen_data, name='screen_calendar'),
    url(r'^addSchedule', views.add_schedule, name='add_schedule'),
    url(r'^getSchedules', views.get_schedules, name='get_schedules'),
]