# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlistManagement', '0004_auto_20160606_0717'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='playlist',
            options={'ordering': ['-last_updated_time']},
        ),
        migrations.AlterModelOptions(
            name='playlistitems',
            options={'ordering': ['position_index']},
        ),
    ]
