# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_auto_20160706_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='total_file_size_limit',
            field=models.BigIntegerField(default=5368709120),
        ),
    ]
