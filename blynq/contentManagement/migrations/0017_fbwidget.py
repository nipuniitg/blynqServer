# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0016_auto_20160928_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='FbWidget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fb_page_url', models.CharField(max_length=250)),
                ('no_of_posts', models.IntegerField(default=10)),
                ('post_duration', models.IntegerField(default=15)),
                ('content', models.ForeignKey(to='contentManagement.Content')),
            ],
        ),
    ]
