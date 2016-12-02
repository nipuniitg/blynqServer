# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('paymentManagement', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paymentduemessage',
            old_name='payment_warning_message',
            new_name='additional_comments',
        ),
        migrations.AddField(
            model_name='paymentduemessage',
            name='due_amount',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='paymentduemessage',
            name='due_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='paymentduemessage',
            name='payment_link',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
