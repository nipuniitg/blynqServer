__author__ = 'PRASANTH'
from django.conf.urls import url
from scheduleManagement import views

urlpatterns = [
     url(r'^$', views.index, name='schedule_index'),
     url(r'^upsertSchedule', views.upsert_schedule, name='upsert_schedule'),
     url(r'^getScreenData/(?P<screen_id>\d+)', views.get_screen_data, name='screen_calendar'),
]