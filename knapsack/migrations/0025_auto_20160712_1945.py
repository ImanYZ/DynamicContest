# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-12 23:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knapsack', '0024_auto_20160627_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='experiment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='knapsack.Experiment'),
        ),
        migrations.AddField(
            model_name='contestusergame',
            name='score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='contestusertraining',
            name='score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='experiment',
            name='contest_number',
            field=models.IntegerField(default=0),
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
