# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_auto_20160803_0558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestedquote',
            name='mobile_number',
            field=models.CharField(max_length=14, null=True, validators=[django.core.validators.RegexValidator(regex=b'^(\\+\\d{1,3}[- ]?)?\\d{10}$', message=b'Invalid Mobile Number, make sure mobile number is 10 digits')]),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='mobile_number',
            field=models.CharField(max_length=14, null=True, validators=[django.core.validators.RegexValidator(regex=b'^(\\+\\d{1,3}[- ]?)?\\d{10}$', message=b'Invalid Mobile Number, make sure mobile number is 10 digits')]),
        ),
    ]
