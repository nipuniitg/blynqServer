# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0004_contenttype'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ContentType',
        ),
    ]
