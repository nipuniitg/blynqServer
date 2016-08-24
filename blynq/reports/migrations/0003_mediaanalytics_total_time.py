# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_auto_20160823_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediaanalytics',
            name='total_time',
            field=models.IntegerField(default=0),
        ),
    ]
