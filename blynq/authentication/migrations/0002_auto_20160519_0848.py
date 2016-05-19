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
            name='total_file_size_limit',
            field=models.BigIntegerField(default=1073741824),
        ),
    ]
