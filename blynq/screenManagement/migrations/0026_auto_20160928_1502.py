# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0025_auto_20160928_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screendatamodified',
            name='screen',
            field=models.OneToOneField(related_name='screen_data_modified', to='screenManagement.Screen'),
        ),
    ]
