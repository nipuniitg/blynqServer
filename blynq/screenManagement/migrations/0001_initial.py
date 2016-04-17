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
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('dummy_screen_group', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(to='authentication.UserDetails', on_delete=django.db.models.deletion.PROTECT)),
                ('organization', models.ForeignKey(to='authentication.Organization', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'ordering': ('-created_on', 'group_name'),
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
                ('activated_on', models.DateField(null=True, blank=True)),
                ('business_type', models.CharField(default=b'PRIVATE', max_length=20, choices=[(b'PRIVATE', b'The screens is bought for private use.'), (b'PUBLIC-SINGLE', b'Only one organization can display advertisement on this screen.'), (b'PUBLIC-SHARED', b'Multiple organization can display advertisement on this screen in slots.')])),
                ('activated_by', models.ForeignKey(blank=True, to='authentication.UserDetails', null=True)),
                ('groups', models.ManyToManyField(to='screenManagement.Group', blank=True)),
                ('location', models.ForeignKey(to='authentication.Address', on_delete=django.db.models.deletion.PROTECT)),
                ('owned_by', models.ManyToManyField(to='authentication.Organization', through='screenManagement.OrganizationScreen')),
                ('placed_by', models.ForeignKey(related_name='screen_placed_by', on_delete=django.db.models.deletion.PROTECT, blank=True, to='authentication.Organization', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScreenSpecs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('brand', models.CharField(max_length=50)),
                ('model_num', models.CharField(max_length=50, null=True, blank=True)),
                ('weight', models.FloatField(null=True, blank=True)),
                ('dimensions', models.CharField(max_length=50, null=True, blank=True)),
                ('resolution', models.CharField(max_length=20, null=True, blank=True)),
                ('display_type', models.CharField(max_length=10, null=True, blank=True)),
                ('screen_size', models.IntegerField()),
                ('aspect_ratio', models.CharField(max_length=20, null=True, blank=True)),
                ('contrast_ratio', models.CharField(max_length=20, null=True, blank=True)),
                ('wattage', models.IntegerField(null=True, blank=True)),
                ('additional_details', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScreenStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status_name', models.CharField(unique=True, max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='screenspecs',
            unique_together=set([('brand', 'model_num')]),
        ),
        migrations.AddField(
            model_name='screen',
            name='specifications',
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
    ]
