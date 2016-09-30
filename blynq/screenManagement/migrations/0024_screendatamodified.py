# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0023_auto_20160830_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScreenDataModified',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_updated_time', models.DateTimeField(auto_now=True, null=True)),
                ('screen', models.ForeignKey(to='screenManagement.Screen')),
            ],
        ),
    ]
