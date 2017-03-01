# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0022_auto_20170301_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='secret_key',
            field=models.CharField(max_length=100, unique=True, null=True, blank=True),
        ),
    ]
