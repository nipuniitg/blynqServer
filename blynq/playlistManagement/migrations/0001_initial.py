# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('contentManagement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('playlist_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('last_updated_time', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('created_by', models.ForeignKey(related_name='playlist_created_by', on_delete=django.db.models.deletion.PROTECT, to='authentication.UserDetails')),
                ('last_updated_by', models.ForeignKey(related_name='playlist_last_updated_by', on_delete=django.db.models.deletion.PROTECT, to='authentication.UserDetails')),
                ('organization', models.ForeignKey(to='authentication.Organization', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlaylistItems',
            fields=[
                ('playlist_items_id', models.AutoField(serialize=False, primary_key=True)),
                ('index', models.IntegerField()),
                ('display_time', models.IntegerField(default=10)),
                ('content', models.ForeignKey(to='contentManagement.Content', on_delete=django.db.models.deletion.PROTECT)),
                ('playlist', models.ForeignKey(to='playlistManagement.Playlist', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
        migrations.AddField(
            model_name='playlist',
            name='playlist_items',
            field=models.ManyToManyField(to='contentManagement.Content', through='playlistManagement.PlaylistItems'),
        ),
    ]
