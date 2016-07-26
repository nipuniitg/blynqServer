# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0017_auto_20160726_1748'),
        ('layoutManagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='layout',
            name='aspect_ratio',
            field=models.ForeignKey(blank=True, to='screenManagement.AspectRatio', null=True),
        ),
    ]
