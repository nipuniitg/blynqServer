# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0005_auto_20160601_1412'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ScreenSpecs',
        ),
    ]
