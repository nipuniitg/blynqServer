# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import paymentManagement.models


class Migration(migrations.Migration):

    dependencies = [
        ('screenManagement', '0030_screen_app_version'),
        ('authentication', '0025_organization_is_active'),
        ('paymentManagement', '0003_paymentduemessage_suspend_access'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerScreen',
            fields=[
                ('customer_screen_id', models.AutoField(serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerSubscription',
            fields=[
                ('customer_subscription_id', models.AutoField(serialize=False, primary_key=True)),
                ('branch_name', models.CharField(max_length=100)),
                ('additional_details', models.TextField(null=True, blank=True)),
                ('screen_monthly_subscription', models.IntegerField(default=500)),
                ('payment_start_date', models.DateField()),
                ('recurring_period', models.IntegerField(default=6, verbose_name=b'in months')),
                ('is_active', models.BooleanField(default=True)),
                ('last_updated_time', models.DateTimeField(auto_now=True, null=True)),
                ('organization', models.ForeignKey(to='authentication.Organization')),
                ('screens', models.ManyToManyField(to='screenManagement.Screen', through='paymentManagement.CustomerScreen')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentInfo',
            fields=[
                ('payment_info_id', models.AutoField(serialize=False, primary_key=True)),
                ('payment_description', models.CharField(max_length=250, null=True, blank=True)),
                ('cycle_start_date', models.DateField()),
                ('total_amount', models.FloatField()),
                ('amount_paid', models.FloatField(default=0)),
                ('is_settled', models.BooleanField(default=False)),
                ('invoice_id', models.CharField(max_length=50, null=True, blank=True)),
                ('invoice', models.FileField(null=True, upload_to=paymentManagement.models.upload_to_invoice_dir, blank=True)),
                ('invoice_sent', models.BooleanField(default=False)),
                ('last_payment_date', models.DateField(null=True, blank=True)),
                ('last_reminder_sent', models.DateField(null=True, blank=True)),
                ('last_updated_time', models.DateTimeField(auto_now=True, null=True)),
                ('customer', models.ForeignKey(to='paymentManagement.CustomerSubscription')),
            ],
        ),
        migrations.AddField(
            model_name='customerscreen',
            name='customer',
            field=models.ForeignKey(to='paymentManagement.CustomerSubscription'),
        ),
        migrations.AddField(
            model_name='customerscreen',
            name='screen',
            field=models.ForeignKey(to='screenManagement.Screen'),
        ),
    ]
