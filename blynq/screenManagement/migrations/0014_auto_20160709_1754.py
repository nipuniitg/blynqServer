# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduleManagement', '0006_auto_20160709_1754'),
        ('screenManagement', '0013_auto_20160709_1717'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='splitscreenpane',
            name='screen_pane',
        ),
        migrations.RemoveField(
            model_name='splitscreenpane',
            name='split_screen',
        ),
        migrations.RemoveField(
            model_name='splitscreen',
            name='split_screen_panes',
        ),
        migrations.AddField(
            model_name='screenpane',
            name='pane_title',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='screenpane',
            name='split_screen',
            field=models.ForeignKey(related_name='screenpane_splitscreen', blank=True, to='screenManagement.SplitScreen', null=True),
        ),
        migrations.DeleteModel(
            name='SplitScreenPane',
        ),
    ]
