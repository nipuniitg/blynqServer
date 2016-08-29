# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0011_auto_20160703_0559'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='length',
            field=models.IntegerField(default=30),
        ),
    ]
