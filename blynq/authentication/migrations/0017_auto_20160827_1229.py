# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_auto_20160827_0723'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='created_on',
            new_name='created_time',
        ),
        migrations.RenameField(
            model_name='userdetails',
            old_name='created_on',
            new_name='created_time',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='last_updated_on',
        ),
        migrations.RemoveField(
            model_name='userdetails',
            name='last_updated_on',
        ),
        migrations.AddField(
            model_name='city',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time', null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time', null=True),
        ),
        migrations.AddField(
            model_name='role',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time', null=True),
        ),
        migrations.AddField(
            model_name='userdetails',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time', null=True),
        ),
    ]
