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
                ('playlist_title', models.CharField(max_length=100)),
                ('playlist_total_time', models.IntegerField()),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('last_updated_time', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('created_by', models.ForeignKey(related_name='playlist_created_by', on_delete=django.db.models.deletion.SET_NULL, to='authentication.UserDetails', null=True)),
                ('last_updated_by', models.ForeignKey(related_name='playlist_last_updated_by', on_delete=django.db.models.deletion.SET_NULL, to='authentication.UserDetails', null=True)),
                ('organization', models.ForeignKey(to='authentication.Organization', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlaylistItems',
            fields=[
                ('playlist_item_id', models.AutoField(serialize=False, primary_key=True)),
                ('position_index', models.IntegerField()),
                ('display_time', models.IntegerField(default=10)),
                ('content', models.ForeignKey(to='contentManagement.Content')),
                ('playlist', models.ForeignKey(to='playlistManagement.Playlist')),
            ],
        ),
        migrations.AddField(
            model_name='playlist',
            name='playlist_items',
            field=models.ManyToManyField(to='contentManagement.Content', through='playlistManagement.PlaylistItems'),
        ),
    ]
