# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0002_auto_20160516_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='file_type',
        ),
        migrations.AddField(
            model_name='content',
            name='document_type',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='file_extension',
            field=models.CharField(max_length=10),
        ),
    ]
