# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0024_screendatamodified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screendatamodified',
            name='screen',
            field=models.ForeignKey(related_name='screen_data_modified', to='screenManagement.Screen'),
        ),
    ]
