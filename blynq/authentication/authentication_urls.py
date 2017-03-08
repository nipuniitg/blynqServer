from django.conf.urls import  url
from django.contrib.auth.views import logout
from authentication import views

urlpatterns = [
    url(r'registerClient', views.create_new_client, name='register_client'),
    url(r'^register', views.register, name='auth_register'),
    url(r'^login', views.login, name='auth_login'),
    url(r'^logout', logout, {'next_page': 'auth_login' }, name='auth_logout'),
    url(r'^getHomePageSummaryJson', views.organization_homepage_summary, name='home_page_summary_json'),
    url(r'^changePassword', views.change_password, name='change_password'),
    url(r'^getUserDetails', views.get_profile_details, name='profile_details'),
    url(r'^updateUserDetails', views.update_user_details, name='update_user_details'),
    url(r'^usernameAvailability', views.username_availability, name='username_availability'),
    url(r'partnerLogin', views.partner_login, name='partner_login'),
    url(r'^checkInstagramUserAccessTokenAvailable', views.check_instagram_user_access_token_available, name="check_instagram_user_access_token_available"),
    url(r'^instagramRedirect', views.instagram_redirect, name='instagram_redirect'),
]