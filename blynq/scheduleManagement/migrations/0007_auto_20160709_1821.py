# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0006_auto_20160709_1754'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedulepane',
            old_name='split_screen_pane',
            new_name='screen_pane',
        ),
    ]
