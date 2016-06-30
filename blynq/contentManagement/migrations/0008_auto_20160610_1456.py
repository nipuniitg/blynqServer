# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0007_auto_20160610_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenttype',
            name='category',
            field=models.CharField(max_length=10, choices=[(b'image', b'Image'), (b'video', b'Video'), (b'pdf', b'Pdf'), (b'gif', b'Gif'), (b'url', b'Url'), (b'iframe', b'Iframe')]),
        ),
    ]
