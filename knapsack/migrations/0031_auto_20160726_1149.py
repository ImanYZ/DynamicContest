# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-26 15:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knapsack', '0030_auto_20160721_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='initializing',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='contestusertraining',
            name='usertraining',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knapsack.Usertraining'),
        ),
        migrations.AlterField(
            model_name='usertrainingitem',
            name='usertraining',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knapsack.Usertraining'),
        ),
    ]
