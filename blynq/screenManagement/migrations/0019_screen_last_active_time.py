# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0018_aspectratio_orientation'),
    ]

    operations = [
        migrations.AddField(
            model_name='screen',
            name='last_active_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 28, 2, 58, 8, 554363, tzinfo=utc)),
        ),
    ]
