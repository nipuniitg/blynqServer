# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0011_auto_20160708_1906'),
    ]

    operations = [
        migrations.RenameField(
            model_name='splitscreen',
            old_name='default_id',
            new_name='layout_id',
        ),
    ]
