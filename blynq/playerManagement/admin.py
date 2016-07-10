from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

# Register your models here.
# Register all the models in the screenManagement app
app = apps.get_app_config('playerManagement')

for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass