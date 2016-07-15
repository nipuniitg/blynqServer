# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0007_auto_20160709_1821'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='split_screen',
            new_name='selected_layout',
        ),
    ]
