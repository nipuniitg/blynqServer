# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0008_auto_20160715_1240'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='selected_layout',
            new_name='split_screen',
        ),
    ]
