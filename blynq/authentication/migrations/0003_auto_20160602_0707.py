# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20160529_1050'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='address',
            name='added_by',
        ),
        migrations.RemoveField(
            model_name='address',
            name='city',
        ),
        migrations.RemoveField(
            model_name='role',
            name='role_description',
        ),
        migrations.AddField(
            model_name='role',
            name='description',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='website',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]
