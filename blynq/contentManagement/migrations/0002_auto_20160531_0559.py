# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='document_type',
            field=models.CharField(default=b'image/jpg', max_length=50, null=True),
        ),
    ]
