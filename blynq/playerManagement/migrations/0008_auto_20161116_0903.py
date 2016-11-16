# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playerManagement', '0007_auto_20160827_1229'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='playerupdate',
            options={'ordering': ['-version', '-uploaded_time']},
        ),
        migrations.AddField(
            model_name='playerupdate',
            name='version',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
