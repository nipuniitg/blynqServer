# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import customLibrary.views_lib


class Migration(migrations.Migration):

    dependencies = [
        ('playlistManagement', '0005_auto_20160610_1418'),
        ('screenManagement', '0022_auto_20160806_1104'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentAnalytics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=customLibrary.views_lib.today_date)),
                ('time_played', models.IntegerField(default=0)),
                ('playlist_item', models.ForeignKey(to='playlistManagement.PlaylistItems', null=True)),
                ('screen', models.ForeignKey(to='screenManagement.Screen', null=True)),
            ],
        ),
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
