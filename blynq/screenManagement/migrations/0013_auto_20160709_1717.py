# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0012_auto_20160709_0450'),
    ]

    operations = [
        migrations.RenameField(
            model_name='splitscreenpane',
            old_name='pane_number',
            new_name='pane_title',
        ),
    ]
