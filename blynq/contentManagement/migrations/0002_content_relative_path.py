# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='relative_path',
            field=models.CharField(default=b'/', max_length=1025),
        ),
    ]
