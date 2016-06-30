# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0005_delete_contenttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentType',
            fields=[
                ('content_type_id', models.AutoField(serialize=False, primary_key=True)),
                ('category', models.CharField(max_length=5, choices=[(b'image', b'Image'), (b'video', b'Video'), (b'pdf', b'Pdf'), (b'gif', b'Gif'), (b'url', b'Url'), (b'iframe', b'Iframe')])),
                ('file_type', models.CharField(max_length=10)),
                ('supported_encodings', models.TextField(help_text=b'list of comma separated encodings', null=True, blank=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='content',
            options={'ordering': ['-last_modified_time']},
        ),
        migrations.AddField(
            model_name='content',
            name='url',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
