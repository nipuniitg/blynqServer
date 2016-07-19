# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0015_remove_splitscreen_layout_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='screenpane',
            old_name='lower_x',
            new_name='left_margin',
        ),
        migrations.RenameField(
            model_name='screenpane',
            old_name='lower_y',
            new_name='top_margin',
        ),
    ]
