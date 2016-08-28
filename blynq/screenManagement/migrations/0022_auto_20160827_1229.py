# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0021_screenanalytics'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupscreens',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time', null=True),
        ),
        migrations.AddField(
            model_name='screenactivationkey',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time', null=True),
        ),
        migrations.AddField(
            model_name='screenanalytics',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time', null=True),
        ),
    ]
