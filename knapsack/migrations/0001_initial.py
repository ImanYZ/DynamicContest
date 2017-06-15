# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-09 12:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vesion', models.IntegerField(default=0)),
                ('skillgroupnum', models.IntegerField(default=0)),
                ('trainingnum', models.IntegerField(default=0)),
                ('gamenum', models.IntegerField(default=0)),
                ('rivalnum', models.IntegerField(default=0)),
                ('maxtime', models.IntegerField(default=0)),
                ('playernum', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.IntegerField(default=0)),
                ('playernum', models.IntegerField(default=0)),
                ('value0', models.IntegerField(default=0)),
                ('weight0', models.IntegerField(default=0)),
                ('value1', models.IntegerField(default=0)),
                ('weight1', models.IntegerField(default=0)),
                ('value2', models.IntegerField(default=0)),
                ('weight2', models.IntegerField(default=0)),
                ('value3', models.IntegerField(default=0)),
                ('weight3', models.IntegerField(default=0)),
                ('value4', models.IntegerField(default=0)),
                ('weight4', models.IntegerField(default=0)),
                ('value5', models.IntegerField(default=0)),
                ('weight5', models.IntegerField(default=0)),
                ('value6', models.IntegerField(default=0)),
                ('weight6', models.IntegerField(default=0)),
                ('value7', models.IntegerField(default=0)),
                ('weight7', models.IntegerField(default=0)),
                ('value8', models.IntegerField(default=0)),
                ('weight8', models.IntegerField(default=0)),
                ('value9', models.IntegerField(default=0)),
                ('weight9', models.IntegerField(default=0)),
                ('value10', models.IntegerField(default=0)),
                ('weight10', models.IntegerField(default=0)),
                ('value11', models.IntegerField(default=0)),
                ('weight11', models.IntegerField(default=0)),
                ('maxseconds', models.IntegerField(default=0)),
                ('maxminutes', models.IntegerField(default=0)),
                ('secondstoreveal', models.IntegerField(default=0)),
                ('minutestoreveal', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knapsack.Experiment')),
            ],
        ),
        migrations.CreateModel(
            name='Gametype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.IntegerField(default=0)),
                ('value0', models.IntegerField(default=0)),
                ('weight0', models.IntegerField(default=0)),
                ('value1', models.IntegerField(default=0)),
                ('weight1', models.IntegerField(default=0)),
                ('value2', models.IntegerField(default=0)),
                ('weight2', models.IntegerField(default=0)),
                ('value3', models.IntegerField(default=0)),
                ('weight3', models.IntegerField(default=0)),
                ('value4', models.IntegerField(default=0)),
                ('weight4', models.IntegerField(default=0)),
                ('value5', models.IntegerField(default=0)),
                ('weight5', models.IntegerField(default=0)),
                ('value6', models.IntegerField(default=0)),
                ('weight6', models.IntegerField(default=0)),
                ('value7', models.IntegerField(default=0)),
                ('weight7', models.IntegerField(default=0)),
                ('value8', models.IntegerField(default=0)),
                ('weight8', models.IntegerField(default=0)),
                ('value9', models.IntegerField(default=0)),
                ('weight9', models.IntegerField(default=0)),
                ('value10', models.IntegerField(default=0)),
                ('weight10', models.IntegerField(default=0)),
                ('value11', models.IntegerField(default=0)),
                ('weight11', models.IntegerField(default=0)),
                ('maxseconds', models.IntegerField(default=0)),
                ('maxminutes', models.IntegerField(default=0)),
                ('secondstoreveal', models.IntegerField(default=0)),
                ('minutestoreveal', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knapsack.Experiment')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=400)),
                ('skill', models.IntegerField(default=0)),
                ('startedstudy', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedstudy', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knapsack.Experiment')),
            ],
        ),
        migrations.CreateModel(
            name='Usergame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tobag0', models.BooleanField(default=0)),
                ('frombag0', models.BooleanField(default=0)),
                ('movetime0', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag1', models.BooleanField(default=0)),
                ('frombag1', models.BooleanField(default=0)),
                ('movetime1', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag2', models.BooleanField(default=0)),
                ('frombag2', models.BooleanField(default=0)),
                ('movetime2', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag3', models.BooleanField(default=0)),
                ('frombag3', models.BooleanField(default=0)),
                ('movetime3', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag4', models.BooleanField(default=0)),
                ('frombag4', models.BooleanField(default=0)),
                ('movetime4', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag5', models.BooleanField(default=0)),
                ('frombag5', models.BooleanField(default=0)),
                ('movetime5', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag6', models.BooleanField(default=0)),
                ('frombag6', models.BooleanField(default=0)),
                ('movetime6', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag7', models.BooleanField(default=0)),
                ('frombag7', models.BooleanField(default=0)),
                ('movetime7', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag8', models.BooleanField(default=0)),
                ('frombag8', models.BooleanField(default=0)),
                ('movetime8', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag9', models.BooleanField(default=0)),
                ('frombag9', models.BooleanField(default=0)),
                ('movetime9', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag10', models.BooleanField(default=0)),
                ('frombag10', models.BooleanField(default=0)),
                ('movetime10', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag11', models.BooleanField(default=0)),
                ('frombag11', models.BooleanField(default=0)),
                ('movetime11', models.DateTimeField(default=django.utils.timezone.now)),
                ('started', models.DateTimeField(default=django.utils.timezone.now)),
                ('finished', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knapsack.Game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knapsack.User')),
            ],
        ),
        migrations.CreateModel(
            name='UserTraining',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tobag0', models.BooleanField(default=0)),
                ('frombag0', models.BooleanField(default=0)),
                ('movetime0', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag1', models.BooleanField(default=0)),
                ('frombag1', models.BooleanField(default=0)),
                ('movetime1', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag2', models.BooleanField(default=0)),
                ('frombag2', models.BooleanField(default=0)),
                ('movetime2', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag3', models.BooleanField(default=0)),
                ('frombag3', models.BooleanField(default=0)),
                ('movetime3', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag4', models.BooleanField(default=0)),
                ('frombag4', models.BooleanField(default=0)),
                ('movetime4', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag5', models.BooleanField(default=0)),
                ('frombag5', models.BooleanField(default=0)),
                ('movetime5', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag6', models.BooleanField(default=0)),
                ('frombag6', models.BooleanField(default=0)),
                ('movetime6', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag7', models.BooleanField(default=0)),
                ('frombag7', models.BooleanField(default=0)),
                ('movetime7', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag8', models.BooleanField(default=0)),
                ('frombag8', models.BooleanField(default=0)),
                ('movetime8', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag9', models.BooleanField(default=0)),
                ('frombag9', models.BooleanField(default=0)),
                ('movetime9', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag10', models.BooleanField(default=0)),
                ('frombag10', models.BooleanField(default=0)),
                ('movetime10', models.DateTimeField(default=django.utils.timezone.now)),
                ('tobag11', models.BooleanField(default=0)),
                ('frombag11', models.BooleanField(default=0)),
                ('movetime11', models.DateTimeField(default=django.utils.timezone.now)),
                ('started', models.DateTimeField(default=django.utils.timezone.now)),
                ('finished', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knapsack.Game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knapsack.User')),
            ],
        ),
    ]
