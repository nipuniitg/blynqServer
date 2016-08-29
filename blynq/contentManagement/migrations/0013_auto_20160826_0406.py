# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0012_content_length'),
    ]

    operations = [
        migrations.RenameField(
            model_name='content',
            old_name='length',
            new_name='duration',
        ),
    ]
