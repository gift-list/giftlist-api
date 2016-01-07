# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-07 17:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventlist',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Address'),
        ),
    ]