# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('screenManagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='screengroups',
            name='created_by',
            field=models.ForeignKey(related_name='screengroups_created_by', on_delete=django.db.models.deletion.SET_NULL, to='authentication.UserDetails', null=True),
        ),
    ]
