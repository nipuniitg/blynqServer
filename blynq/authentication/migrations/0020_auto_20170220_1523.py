# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0019_organization_total_screen_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='organization_name',
            field=models.CharField(max_length=100, db_index=True),
        ),
    ]
