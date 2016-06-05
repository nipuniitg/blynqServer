# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0003_delete_contenttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentType',
            fields=[
                ('content_type_id', models.AutoField(serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=3, choices=[(b'IMG', b'Image'), (b'VID', b'Video'), (b'PPT', b'Presentation'), (b'PDF', b'Pdf'), (b'GIF', b'Gif')])),
                ('file_extension', models.CharField(max_length=10)),
            ],
        ),
    ]
