# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-16 11:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knapsack', '0011_auto_20160514_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergame',
            name='submitted',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='usertraining',
            name='submitted',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='usertrainingitem',
            name='usertraining',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knapsack.Usertraining'),
        ),
    ]
