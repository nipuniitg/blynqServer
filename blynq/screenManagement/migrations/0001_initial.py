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
                ('group_id', models.AutoField(serialize=False, primary_key=True)),
                ('group_name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to='authentication.UserDetails', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'ordering': ('-created_on', 'group_name'),
            },
        ),
        migrations.CreateModel(
            name='Screen',
            fields=[
                ('screen_id', models.AutoField(serialize=False, primary_key=True)),
                ('screen_name', models.CharField(max_length=100)),
                ('screen_size', models.IntegerField(blank=True)),
                ('aspect_ratio', models.CharField(max_length=20, null=True, blank=True)),
                ('resolution', models.CharField(max_length=20, null=True, blank=True)),
                ('address', models.CharField(max_length=100, blank=True)),
                ('device_identification_id', models.CharField(max_length=16, null=True, blank=True)),
                ('activation_key', models.CharField(max_length=16)),
                ('activated_on', models.DateField(null=True, blank=True)),
                ('business_type', models.CharField(default=b'PRIVATE', max_length=20, choices=[(b'PRIVATE', b'The screens is bought for private use.'), (b'PUBLIC-PRIVATE', b'Only one organization can display advertisement on this screen.'), (b'PUBLIC-SHARED', b'Multiple organization can display advertisement on this screen in slots.')])),
                ('activated_by', models.ForeignKey(blank=True, to='authentication.UserDetails', null=True)),
                ('groups', models.ManyToManyField(to='screenManagement.Group', blank=True)),
                ('owned_by', models.ForeignKey(to='authentication.Organization', null=True)),
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
                ('display_type', models.CharField(max_length=10, null=True, blank=True)),
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
    ]
