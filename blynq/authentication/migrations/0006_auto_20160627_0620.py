# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_localserver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localserver',
            name='unique_key',
            field=models.CharField(help_text=b'Enter the MAC-Address of the device as unique key', max_length=30),
        ),
    ]
