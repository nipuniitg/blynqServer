# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0019_instagramwidget'),
    ]

    operations = [
        migrations.CreateModel(
            name='RssUrlWidget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rss_url', models.CharField(max_length=250)),
                ('background_color', models.CharField(default=b'#000', max_length=7, null=True, blank=True)),
                ('font_color', models.CharField(default=b'#fff', max_length=7, null=True, blank=True)),
                ('content', models.OneToOneField(to='contentManagement.Content')),
            ],
        ),
        migrations.CreateModel(
            name='ScrollTextWidget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('widget_text', models.TextField(null=True, blank=True)),
                ('background_color', models.CharField(default=b'#000', max_length=7, null=True, blank=True)),
                ('font_color', models.CharField(default=b'#fff', max_length=7, null=True, blank=True)),
                ('content', models.OneToOneField(to='contentManagement.Content')),
            ],
        ),
    ]
