# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0009_auto_20160614_1117'),
    ]

    operations = [
        migrations.CreateModel(
            name='SplitScreen',
            fields=[
                ('split_screen_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100)),
            ],
        ),
    ]
