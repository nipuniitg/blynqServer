# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0013_auto_20160826_0406'),
    ]

    operations = [
        migrations.RenameField(
            model_name='content',
            old_name='last_modified_by',
            new_name='last_updated_by',
        ),
        migrations.RemoveField(
            model_name='content',
            name='last_modified_time',
        ),
        migrations.AddField(
            model_name='content',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time', null=True),
        ),
    ]
