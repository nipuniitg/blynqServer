# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0010_splitscreen'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScreenPane',
            fields=[
                ('screen_pane_id', models.AutoField(serialize=False, primary_key=True)),
                ('lower_x', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('lower_y', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('width', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('height', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
            ],
        ),
        migrations.CreateModel(
            name='SplitScreenPane',
            fields=[
                ('split_pane_id', models.AutoField(serialize=False, primary_key=True)),
                ('pane_number', models.CharField(max_length=30, null=True, blank=True)),
                ('screen_pane', models.ForeignKey(to='screenManagement.ScreenPane')),
            ],
        ),
        migrations.AddField(
            model_name='splitscreen',
            name='default_id',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='splitscreen',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='splitscreen',
            name='num_of_panes',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='splitscreenpane',
            name='split_screen',
            field=models.ForeignKey(to='screenManagement.SplitScreen'),
        ),
        migrations.AddField(
            model_name='splitscreen',
            name='split_screen_panes',
            field=models.ManyToManyField(to='screenManagement.ScreenPane', through='screenManagement.SplitScreenPane'),
        ),
    ]
