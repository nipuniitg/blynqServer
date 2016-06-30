# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_localserver'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='name',
            new_name='organization_name',
        ),
        migrations.AlterField(
            model_name='localserver',
            name='unique_key',
            field=models.CharField(help_text=b'Enter the decimal format of MAC-Address of the device as unique key', max_length=20),
        ),
    ]
