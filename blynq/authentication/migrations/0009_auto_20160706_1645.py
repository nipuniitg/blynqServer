# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_playerupdate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='localserver',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='playerupdate',
            name='uploaded_by',
        ),
        migrations.DeleteModel(
            name='LocalServer',
        ),
        migrations.DeleteModel(
            name='PlayerUpdate',
        ),
    ]
