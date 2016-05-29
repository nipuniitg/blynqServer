# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('screenManagement', '0003_auto_20160529_0716'),
    ]

    operations = [
        migrations.AddField(
            model_name='screen',
            name='city',
            field=models.ForeignKey(blank=True, to='authentication.City', null=True),
        ),
    ]
