# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0028_auto_20161019_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='screen',
            name='update_app',
            field=models.BooleanField(default=False),
        ),
    ]
