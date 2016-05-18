# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('screenManagement', '0002_screengroups_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupScreens',
            fields=[
                ('group_screen_id', models.AutoField(serialize=False, primary_key=True)),
                ('created_by', models.ForeignKey(related_name='groupscreens_created_by', on_delete=django.db.models.deletion.SET_NULL, to='authentication.UserDetails', null=True)),
                ('group', models.ForeignKey(to='screenManagement.Group')),
            ],
        ),
        migrations.RemoveField(
            model_name='screengroups',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='screengroups',
            name='group',
        ),
        migrations.RemoveField(
            model_name='screengroups',
            name='screen',
        ),
        migrations.AlterField(
            model_name='screen',
            name='groups',
            field=models.ManyToManyField(to='screenManagement.Group', through='screenManagement.GroupScreens', blank=True),
        ),
        migrations.DeleteModel(
            name='ScreenGroups',
        ),
        migrations.AddField(
            model_name='groupscreens',
            name='screen',
            field=models.ForeignKey(to='screenManagement.Screen'),
        ),
    ]
