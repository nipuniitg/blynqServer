from django.conf.urls import url

import layoutManagement.views
from screenManagement import views

urlpatterns = [
    url(r'^getLayouts', layoutManagement.views.get_layouts, name='get_layouts'),
]