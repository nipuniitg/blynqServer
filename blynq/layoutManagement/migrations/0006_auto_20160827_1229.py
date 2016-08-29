# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0017_auto_20160827_1229'),
        ('layoutManagement', '0005_auto_20160814_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='layout',
            name='created_by',
            field=models.ForeignKey(related_name='layout_created_by', on_delete=django.db.models.deletion.SET_NULL, to='authentication.UserDetails', null=True),
        ),
        migrations.AddField(
            model_name='layout',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created time', null=True),
        ),
        migrations.AddField(
            model_name='layout',
            name='last_updated_by',
            field=models.ForeignKey(related_name='layout_last_updated_by', on_delete=django.db.models.deletion.SET_NULL, to='authentication.UserDetails', null=True),
        ),
        migrations.AddField(
            model_name='layout',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time', null=True),
        ),
        migrations.AddField(
            model_name='layoutpane',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time', null=True),
        ),
    ]
