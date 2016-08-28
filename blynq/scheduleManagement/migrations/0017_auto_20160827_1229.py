# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0016_schedulepane_mute_audio'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedulepane',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time', null=True),
        ),
        migrations.AddField(
            model_name='scheduleplaylists',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time', null=True),
        ),
        migrations.AddField(
            model_name='schedulescreens',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time', null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created time', null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time', null=True),
        ),
    ]
