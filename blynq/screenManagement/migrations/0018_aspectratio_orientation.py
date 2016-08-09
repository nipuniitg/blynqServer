# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0017_auto_20160726_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='aspectratio',
            name='orientation',
            field=models.CharField(default=b'LANDSCAPE', max_length=20, choices=[(b'LANDSCAPE', b'Landscape Orientation'), (b'PORTRAIT', b'Portrait Orientation')]),
        ),
    ]
