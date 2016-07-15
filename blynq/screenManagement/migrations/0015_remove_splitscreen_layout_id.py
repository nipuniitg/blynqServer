# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0014_auto_20160709_1754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='splitscreen',
            name='layout_id',
        ),
    ]
