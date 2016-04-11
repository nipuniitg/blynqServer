# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='contact',
            field=models.CharField(max_length=12, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='mobile_number',
            field=models.CharField(max_length=12),
        ),
    ]
