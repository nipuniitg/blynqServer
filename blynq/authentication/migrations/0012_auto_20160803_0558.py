# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_auto_20160803_0554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestedquote',
            name='mobile_number',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='mobile_number',
            field=models.CharField(max_length=12, null=True),
        ),
    ]
