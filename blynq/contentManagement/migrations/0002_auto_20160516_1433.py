# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contenttype',
            old_name='fileExtension',
            new_name='file_extension',
        ),
    ]
