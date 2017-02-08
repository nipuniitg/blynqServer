# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0017_fbwidget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fbwidget',
            name='content',
            field=models.OneToOneField(to='contentManagement.Content'),
        ),
    ]
