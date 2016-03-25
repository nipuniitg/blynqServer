# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_remove_organization_vid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('filename', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('last_modified_time', models.DateTimeField()),
                ('is_folder', models.BooleanField()),
                ('directory_path', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='ContentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=3, choices=[(b'IMG', b'Image'), (b'VID', b'Video'), (b'PPT', b'Presentation'), (b'GIF', b'Gif')])),
                ('fileExtension', models.CharField(max_length=5)),
            ],
        ),
        migrations.AddField(
            model_name='content',
            name='file_type',
            field=models.ForeignKey(to='contentManagement.ContentType', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='content',
            name='last_modified_by',
            field=models.ForeignKey(related_name='content_modified_by', on_delete=django.db.models.deletion.PROTECT, to='authentication.UserDetails'),
        ),
        migrations.AddField(
            model_name='content',
            name='uploaded_by',
            field=models.ForeignKey(related_name='content_uploaded_by', on_delete=django.db.models.deletion.PROTECT, to='authentication.UserDetails'),
        ),
    ]
