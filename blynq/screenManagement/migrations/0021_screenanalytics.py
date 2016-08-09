# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import customLibrary.views_lib


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0020_auto_20160728_0320'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScreenAnalytics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=customLibrary.views_lib.today_date)),
                ('time_online', models.PositiveIntegerField(default=0)),
                ('screen', models.ForeignKey(related_name='screenanalytics_screen', to='screenManagement.Screen')),
            ],
        ),
    ]
