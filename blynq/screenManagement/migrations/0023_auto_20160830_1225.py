# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0022_auto_20160827_1229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='screenanalytics',
            name='screen',
        ),
        migrations.DeleteModel(
            name='ScreenAnalytics',
        ),
    ]
