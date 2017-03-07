# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0023_auto_20170301_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccessTokens',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instagram_access_token', models.CharField(max_length=250, null=True, blank=True)),
                ('user_details', models.OneToOneField(to='authentication.UserDetails')),
            ],
        ),
    ]
