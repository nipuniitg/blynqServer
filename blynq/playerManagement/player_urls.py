from django.conf.urls import url
from playerManagement import views

urlpatterns = [
    url(r'^getScreenData', views.get_screen_data, name='screen_calendar'),
    url(r'^getContentUrlsLocal', views.get_content_urls_local, name='get_content_urls_local'),
    url(r'^activationKeyValid', views.activation_key_valid, name='activation_key_valid'),
    url(r'^updateAvailable', views.player_update_available, name='player_update_available'),
]