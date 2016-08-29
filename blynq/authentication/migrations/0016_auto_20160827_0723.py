# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0015_auto_20160824_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='total_file_size_limit',
            field=models.BigIntegerField(default=1073741824),
        ),
        migrations.AlterField(
            model_name='organization',
            name='website',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
