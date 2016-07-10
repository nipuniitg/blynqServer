# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import playerManagement.models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_auto_20160706_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalServer',
            fields=[
                ('local_server_id', models.AutoField(serialize=False, primary_key=True)),
                ('local_url', models.CharField(max_length=255)),
                ('unique_key', models.CharField(help_text=b'Enter the decimal format of MAC-Address of the device as unique key', max_length=20)),
                ('organization', models.ForeignKey(to='authentication.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerUpdate',
            fields=[
                ('player_update_id', models.AutoField(serialize=False, primary_key=True)),
                ('executable', models.FileField(upload_to=playerManagement.models.upload_to_dir)),
                ('comments', models.TextField(null=True, blank=True)),
                ('uploaded_time', models.DateTimeField(auto_now_add=True, verbose_name='uploaded time')),
                ('last_modified_time', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('uploaded_by', models.ForeignKey(related_name='playerupdate_uploaded_by', on_delete=django.db.models.deletion.SET_NULL, to='authentication.UserDetails', null=True)),
            ],
            options={
                'ordering': ['-uploaded_time'],
            },
        ),
    ]
