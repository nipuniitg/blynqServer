__author__ = 'PRASANTH'
from django.conf.urls import url
from scheduleManagement import views

urlpatterns = [
     url(r'^$', views.index, name = 'schedule_index'),
]