# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Layout',
            fields=[
                ('layout_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('is_default', models.BooleanField(default=False)),
                ('num_of_panes', models.IntegerField(default=2)),
            ],
        ),
        migrations.CreateModel(
            name='LayoutPane',
            fields=[
                ('layout_pane_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('left_margin', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('top_margin', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('z_index', models.IntegerField()),
                ('width', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('height', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('layout', models.ForeignKey(related_name='layoutpane_layout', blank=True, to='layoutManagement.Layout', null=True)),
            ],
        ),
    ]
