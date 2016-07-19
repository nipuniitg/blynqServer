# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0009_auto_20160715_1241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedulescreens',
            name='event',
        ),
    ]
