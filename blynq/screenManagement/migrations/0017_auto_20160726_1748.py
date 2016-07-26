# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0011_auto_20160726_1748'),
        ('screenManagement', '0016_auto_20160719_0638'),
    ]

    operations = [
        migrations.CreateModel(
            name='AspectRatio',
            fields=[
                ('aspect_ratio_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('width_component', models.IntegerField()),
                ('height_component', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='screenpane',
            name='split_screen',
        ),
        migrations.DeleteModel(
            name='ScreenPane',
        ),
        migrations.DeleteModel(
            name='SplitScreen',
        ),
    ]
