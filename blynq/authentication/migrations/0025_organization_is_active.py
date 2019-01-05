# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0024_organization_enable_reports'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
