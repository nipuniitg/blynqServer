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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='name')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('document', models.FileField(upload_to=contentManagement.models.upload_to_dir)),
                ('_file_size', models.IntegerField(null=True, verbose_name='file size', blank=True)),
                ('sha1_hash', models.CharField(default=b'', max_length=40, verbose_name='sha1', blank=True)),
                ('original_filename', models.CharField(max_length=100, null=True, verbose_name='original filename', blank=True)),
                ('uploaded_time', models.DateTimeField(auto_now_add=True, verbose_name='uploaded time')),
                ('last_modified_time', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('is_public', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=3, choices=[(b'IMG', b'Image'), (b'VID', b'Video'), (b'PPT', b'Presentation'), (b'PDF', b'Pdf'), (b'GIF', b'Gif')])),
                ('fileExtension', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='uploaded at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('dummy_content_folder', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(related_name='filer_owned_folders', verbose_name=b'owner', blank=True, to='authentication.UserDetails', null=True)),
                ('parent', models.ForeignKey(related_name='children', verbose_name=b'parent', blank=True, to='contentManagement.Folder', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='content',
            name='file_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contentManagement.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='folder',
            field=models.ForeignKey(related_name='all_files', verbose_name='folder', blank=True, to='contentManagement.Folder', null=True),
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
