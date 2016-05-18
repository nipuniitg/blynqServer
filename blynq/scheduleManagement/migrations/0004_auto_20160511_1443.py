# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0003_auto_20160511_0731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedulescreens',
            name='screen',
            field=models.ForeignKey(related_name='schedulescreens_screen_id', blank=True, to='screenManagement.Screen', null=True),
        ),
    ]
