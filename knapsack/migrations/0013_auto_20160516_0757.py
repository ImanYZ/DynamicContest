# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-16 11:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knapsack', '0012_auto_20160516_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertrainingitem',
            name='usertraining',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knapsack.Usertraining'),
        ),
    ]