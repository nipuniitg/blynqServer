from django.conf.urls import url

import layoutManagement.views as views

urlpatterns = [
    url(r'^getLayouts', views.get_layouts, name='get_layouts'),
    url(r'^getDefaultLayouts', views.get_default_layouts, name='get_default_layouts'),
    url(r'^upsertLayout', views.upsert_layout, name='upsert_layout'),
    url(r'^deleteLayout', views.delete_layout, name='delete_layout'),
]