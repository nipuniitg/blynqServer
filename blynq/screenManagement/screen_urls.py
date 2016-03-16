__author__ = 'PRASANTH'
from django.conf.urls import url
from screenManagement import views

urlpatterns = [
     url(r'^$', views.index, name = 'screen_index'),
]