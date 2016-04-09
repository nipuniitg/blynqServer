# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('playlistManagement', '0001_initial'),
        ('screenManagement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('last_updated_time', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('created_by', models.ForeignKey(related_name='schedule_created_by', on_delete=django.db.models.deletion.PROTECT, to='authentication.UserDetails')),
                ('last_updated_by', models.ForeignKey(related_name='schedule_last_updated_by', on_delete=django.db.models.deletion.PROTECT, to='authentication.UserDetails')),
                ('playlist', models.ForeignKey(to='playlistManagement.Playlist', on_delete=django.db.models.deletion.PROTECT)),
                ('screens', models.ManyToManyField(to='screenManagement.Group')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='schedule',
            field=models.ForeignKey(to='scheduleManagement.Schedule', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
