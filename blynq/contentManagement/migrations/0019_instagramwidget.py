# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentManagement', '0018_auto_20170208_1552'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramWidget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('no_of_posts', models.IntegerField(default=10)),
                ('post_duration', models.IntegerField(default=15)),
                ('content', models.OneToOneField(to='contentManagement.Content')),
            ],
        ),
    ]
