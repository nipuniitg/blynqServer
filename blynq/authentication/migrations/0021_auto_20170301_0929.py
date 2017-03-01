# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0020_auto_20170220_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='parent',
            field=models.ForeignKey(blank=True, to='authentication.Organization', null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='secret_key',
            field=models.CharField(max_length=24, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='use_blynq_banner',
            field=models.BooleanField(default=True),
        ),
    ]
