# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0027_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screenactivationkey',
            name='activation_key',
            field=models.CharField(unique=True, max_length=16, db_index=True),
        ),
    ]
