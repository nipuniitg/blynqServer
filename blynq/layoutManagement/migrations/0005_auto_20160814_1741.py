# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-14 17:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('layoutManagement', '0004_auto_20160726_1943'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='layout',
            options={'ordering': ['layout_id']},
        ),
    ]