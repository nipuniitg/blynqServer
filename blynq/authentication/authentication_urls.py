from django.conf.urls import  url
from authentication import views

urlpatterns = [
     # url(r'^register', views.register, name = 'auth_register'),
     url(r'^login', views.login, name='auth_login'),
     url(r'^logout', 'django.contrib.auth.views.logout', {'next_page': 'auth_login' }, name='auth_logout'),
     url(r'^getHomePageSummaryJson', views.organization_homepage_summary, name='home_page_summary_json'),
     url(r'^getPlayerUpdate', views.get_player_update, name='get_player_update')
]