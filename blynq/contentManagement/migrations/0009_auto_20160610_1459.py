# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0008_auto_20160610_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenttype',
            name='file_type',
            field=models.CharField(max_length=30),
        ),
    ]
