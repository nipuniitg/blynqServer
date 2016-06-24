# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0008_auto_20160614_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='screen',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
