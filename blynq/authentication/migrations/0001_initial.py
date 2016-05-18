# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('address_id', models.AutoField(serialize=False, primary_key=True)),
                ('building_name', models.CharField(max_length=100)),
                ('address_line1', models.CharField(max_length=100, blank=True)),
                ('address_line2', models.CharField(max_length=100, blank=True)),
                ('area', models.CharField(max_length=100)),
                ('landmark', models.CharField(max_length=100)),
                ('pincode', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('city_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('state', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('organization_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('website', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100, null=True, blank=True)),
                ('contact', models.CharField(max_length=12, null=True, blank=True)),
                ('total_file_size_limit', models.BigIntegerField(default=5368709120)),
                ('used_file_size', models.BigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='RequestedQuote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('mobile_number', models.CharField(max_length=12)),
                ('num_of_devices', models.IntegerField()),
                ('additional_details', models.TextField(null=True, blank=True)),
                ('requested_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_id', models.AutoField(serialize=False, primary_key=True)),
                ('role_name', models.CharField(unique=True, max_length=50)),
                ('role_description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('mobile_number', models.CharField(max_length=12)),
                ('organization', models.ForeignKey(to='authentication.Organization')),
                ('role', models.ForeignKey(to='authentication.Role')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='added_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='authentication.UserDetails', null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(to='authentication.City', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set([('building_name', 'added_by')]),
        ),
    ]
