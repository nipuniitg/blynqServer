# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0006_auto_20160610_1418'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='document_type',
        ),
        migrations.RemoveField(
            model_name='content',
            name='original_filename',
        ),
        migrations.AddField(
            model_name='content',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contentManagement.ContentType', null=True),
        ),
    ]
