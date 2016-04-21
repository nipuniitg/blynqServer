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
                ('document', models.FileField(null=True, upload_to=contentManagement.models.upload_to_dir)),
                ('sha1_hash', models.CharField(default=b'', max_length=40, verbose_name='sha1', blank=True)),
                ('original_filename', models.CharField(max_length=100, null=True, verbose_name='original filename', blank=True)),
                ('uploaded_time', models.DateTimeField(auto_now_add=True, verbose_name='uploaded time')),
                ('last_modified_time', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('is_folder', models.BooleanField(default=False)),
                ('relative_path', models.CharField(default=b'/', max_length=1025)),
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
        migrations.AddField(
            model_name='content',
            name='file_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contentManagement.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='last_modified_by',
            field=models.ForeignKey(related_name='content_modified_by', on_delete=django.db.models.deletion.PROTECT, to='authentication.UserDetails'),
        ),
        migrations.AddField(
            model_name='content',
            name='organization',
            field=models.ForeignKey(to='authentication.Organization', null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='parent_folder',
            field=models.ForeignKey(to='contentManagement.Content', null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='uploaded_by',
            field=models.ForeignKey(related_name='content_uploaded_by', on_delete=django.db.models.deletion.PROTECT, to='authentication.UserDetails'),
        ),
        migrations.AlterUniqueTogether(
            name='content',
            unique_together=set([('title', 'parent_folder', 'uploaded_by')]),
        ),
    ]
