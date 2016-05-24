# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import contentManagement.models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('content_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='name')),
                ('document', models.FileField(null=True, upload_to=contentManagement.models.upload_to_dir)),
                ('sha1_hash', models.CharField(default=b'', max_length=40, verbose_name='sha1', blank=True)),
                ('original_filename', models.CharField(max_length=100, null=True, verbose_name='original filename', blank=True)),
                ('document_type', models.CharField(default=b'image/jpg', max_length=50)),
                ('uploaded_time', models.DateTimeField(auto_now_add=True, verbose_name='uploaded time')),
                ('last_modified_time', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('is_folder', models.BooleanField(default=False)),
                ('relative_path', models.CharField(default=b'/', max_length=1025)),
                ('last_modified_by', models.ForeignKey(related_name='content_modified_by', on_delete=django.db.models.deletion.SET_NULL, to='authentication.UserDetails', null=True)),
                ('organization', models.ForeignKey(to='authentication.Organization', null=True)),
                ('parent_folder', models.ForeignKey(to='contentManagement.Content', null=True)),
                ('uploaded_by', models.ForeignKey(related_name='content_uploaded_by', on_delete=django.db.models.deletion.SET_NULL, to='authentication.UserDetails', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContentType',
            fields=[
                ('content_type_id', models.AutoField(serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=3, choices=[(b'IMG', b'Image'), (b'VID', b'Video'), (b'PPT', b'Presentation'), (b'PDF', b'Pdf'), (b'GIF', b'Gif')])),
                ('file_extension', models.CharField(max_length=10)),
            ],
        ),
    ]
