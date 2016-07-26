# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('layoutManagement', '0003_layout_organization'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='layout',
            name='num_of_panes',
        ),
        migrations.AlterField(
            model_name='layout',
            name='organization',
            field=models.ForeignKey(related_name='layout_organization', blank=True, to='authentication.Organization', null=True),
        ),
    ]
