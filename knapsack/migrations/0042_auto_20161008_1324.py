# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-08 17:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knapsack', '0041_auto_20161008_1025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiment',
            name='group1_current_Contest_index',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='group2_current_Contest_index',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='group3_current_Contest_index',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='group4_current_Contest_index',
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