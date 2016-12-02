# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0018_auto_20161019_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentDueMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('show_warning', models.BooleanField(default=False)),
                ('payment_warning_message', models.CharField(default=b'', max_length=250, blank=True)),
                ('organization', models.OneToOneField(to='authentication.Organization')),
            ],
        ),
    ]
