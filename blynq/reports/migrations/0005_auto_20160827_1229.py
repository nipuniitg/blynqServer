# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_auto_20160824_0655'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediaanalytics',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time', null=True),
        ),
        migrations.AddField(
            model_name='screenanalytics',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time', null=True),
        ),
    ]
