# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-28 18:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knapsack', '0043_auto_20161013_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='infeasible',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contest',
            name='infeasiblility20Percent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contest',
            name='infeasiblility40Percent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='game',
            name='gametype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='knapsack.Gametype'),
        ),
        migrations.AddField(
            model_name='game',
            name='infeasiblility20Percent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='game',
            name='infeasiblility40Percent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='gametype',
            name='max_score_ratio',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='gametype',
            name='min_score_ratio',
            field=models.FloatField(default=0),
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
