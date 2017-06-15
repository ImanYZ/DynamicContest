# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-06 18:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knapsack', '0039_auto_20161006_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='initializing',
            field=models.BooleanField(default=False),
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
