# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_auto_20160808_0700'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='last_updated_on',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='userdetails',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='userdetails',
            name='last_updated_on',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
