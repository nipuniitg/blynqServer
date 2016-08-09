# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_auto_20160706_1645'),
        ('layoutManagement', '0002_layout_aspect_ratio'),
    ]

    operations = [
        migrations.AddField(
            model_name='layout',
            name='organization',
            field=models.ForeignKey(blank=True, to='authentication.Organization', null=True),
        ),
    ]
