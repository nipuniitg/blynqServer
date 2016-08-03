# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_auto_20160728_0258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestedquote',
            name='mobile_number',
            field=models.BigIntegerField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='mobile_number',
            field=models.BigIntegerField(max_length=10, null=True),
        ),
    ]
