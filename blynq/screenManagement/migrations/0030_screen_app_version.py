# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0029_screen_update_app'),
    ]

    operations = [
        migrations.AddField(
            model_name='screen',
            name='app_version',
            field=models.IntegerField(default=1, null=True, blank=True),
        ),
    ]
