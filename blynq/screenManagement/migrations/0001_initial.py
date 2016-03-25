# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('building_name', models.CharField(max_length=100)),
                ('line1', models.CharField(max_length=100)),
                ('line2', models.CharField(max_length=100)),
                ('area', models.CharField(max_length=100)),
                ('landmark', models.CharField(max_length=100)),
                ('pincode', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='BusinessType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('created_on', models.DateField()),
                ('created_by', models.ForeignKey(to='authentication.UserDetails', on_delete=django.db.models.deletion.PROTECT)),
                ('organization', models.ForeignKey(to='authentication.Organization', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'ordering': ('-created_on', 'name'),
            },
        ),
        migrations.CreateModel(
            name='OrganizationScreen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('time_slot_valid', models.BooleanField()),
                ('time_slot', models.IntegerField(null=True)),
                ('organization', models.ForeignKey(to='authentication.Organization', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
        migrations.CreateModel(
            name='Screen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('screen_name', models.CharField(max_length=100)),
                ('activation_key', models.CharField(max_length=16)),
                ('activated_on', models.DateField()),
                ('business_type', models.ForeignKey(to='screenManagement.BusinessType', on_delete=django.db.models.deletion.PROTECT)),
                ('groups', models.ManyToManyField(to='screenManagement.Group')),
                ('location', models.ForeignKey(to='screenManagement.Address', on_delete=django.db.models.deletion.PROTECT)),
                ('owned_by', models.ManyToManyField(to='authentication.Organization', through='screenManagement.OrganizationScreen')),
                ('placed_by', models.ForeignKey(related_name='screen_placed_by', on_delete=django.db.models.deletion.PROTECT, to='authentication.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='ScreenSpecs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('brand', models.CharField(max_length=50, null=True)),
                ('model_num', models.CharField(max_length=50, null=True)),
                ('weight', models.FloatField(null=True)),
                ('dimensions', models.CharField(max_length=50, null=True)),
                ('resolution', models.CharField(max_length=20)),
                ('display_type', models.CharField(max_length=10, null=True)),
                ('size', models.IntegerField()),
                ('aspect_ratio', models.CharField(max_length=20, null=True)),
                ('contrast_ratio', models.CharField(max_length=20, null=True)),
                ('wattage', models.IntegerField(null=True)),
                ('additional_details', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScreenStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='screen',
            name='specs',
            field=models.ForeignKey(to='screenManagement.ScreenSpecs', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='screen',
            name='status',
            field=models.ForeignKey(to='screenManagement.ScreenStatus', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='organizationscreen',
            name='screen',
            field=models.ForeignKey(to='screenManagement.Screen', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(to='screenManagement.City', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
