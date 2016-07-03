# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0010_remove_contenttype_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={},
        ),
    ]
