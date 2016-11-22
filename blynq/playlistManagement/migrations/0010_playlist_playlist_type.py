# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlistManagement', '0009_auto_20160928_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='playlist_type',
            field=models.CharField(default=b'user_created', max_length=20, choices=[(b'user_created', b'Playlist created by the User/organization'), (b'widget', b'Playlist automatically created from widget'), (b'content', b'Playlist automatically created from uploaded content'), (b'blynq_tv', b'Playlist created by the BlynQ organization')]),
        ),
    ]
