# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20160603_0655'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalServer',
            fields=[
                ('local_server_id', models.AutoField(serialize=False, primary_key=True)),
                ('local_url', models.CharField(max_length=255)),
                ('unique_key', models.CharField(max_length=30)),
                ('organization', models.ForeignKey(to='authentication.Organization')),
            ],
        ),
    ]
