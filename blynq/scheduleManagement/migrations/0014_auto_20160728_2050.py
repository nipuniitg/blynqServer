# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0013_auto_20160728_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedulepane',
            name='layout_pane',
            field=models.ForeignKey(blank=True, to='layoutManagement.LayoutPane', null=True),
        ),
    ]
