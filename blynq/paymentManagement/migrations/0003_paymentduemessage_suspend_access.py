# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paymentManagement', '0002_auto_20161202_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentduemessage',
            name='suspend_access',
            field=models.BooleanField(default=False),
        ),
    ]
