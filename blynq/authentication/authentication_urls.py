from django.conf.urls import  url
from django.contrib.auth.views import logout
from authentication import views

urlpatterns = [
     # url(r'^register', views.register, name = 'auth_register'),
     url(r'^login', views.login, name='auth_login'),
     url(r'^logout', logout, {'next_page': 'auth_login' }, name='auth_logout'),
     url(r'^getHomePageSummaryJson', views.organization_homepage_summary, name='home_page_summary_json'),
     url(r'^changePassword', views.change_password, name='change_password'),
     url(r'^getUserDetails', views.get_profile_details, name='profile_details'),
     url(r'^updateUserDetails', views.update_user_details, name='update_user_details'),
]