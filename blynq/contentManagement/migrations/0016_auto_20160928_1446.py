# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0015_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='duration',
            field=models.IntegerField(default=15),
        ),
    ]
