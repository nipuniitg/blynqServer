# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0018_auto_20161019_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='total_screen_count',
            field=models.IntegerField(default=0),
        ),
    ]
