# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0009_auto_20160610_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contenttype',
            name='category',
        ),
    ]
