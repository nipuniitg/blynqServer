# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-12 12:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlistManagement', '0006_playlist_user_visible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlistitems',
            name='position_index',
            field=models.IntegerField(default=0),
        ),
    ]
