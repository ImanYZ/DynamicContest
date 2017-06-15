# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-13 18:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knapsack', '0050_auto_20170612_0115'),
    ]

    operations = [
        migrations.CreateModel(
            name='Userquitquestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('why_quit', models.TextField(blank=True, null=True)),
                ('feasible', models.BooleanField(default=False)),
                ('infeasible', models.BooleanField(default=False)),
                ('correct', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='userquitquesstion',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userquiz',
            name='user',
        ),
        migrations.AddField(
            model_name='user',
            name='Feasible60Infeasible40',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='Feasible60NotSure',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='Feasible60Target40',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='GroupSize12',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='GroupSize3',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='GroupSize4',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='GroupSizeNotSure',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='InfeasibleIsSolvableFalse',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='InfeasibleIsSolvableNotSure',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='InfeasibleIsSolvableTrue',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='SameOpponentNo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='SameOpponentNotSure',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='SameOpponentYes',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='SureGameFalse',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='SureGameNotSure',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='SureGameTrue',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='quit_question_earning',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='quiz_earning',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='quizscore',
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
        migrations.DeleteModel(
            name='Userquitquesstion',
        ),
        migrations.DeleteModel(
            name='Userquiz',
        ),
        migrations.AddField(
            model_name='userquitquestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knapsack.User'),
        ),
        migrations.AddField(
            model_name='userquitquestion',
            name='usergame',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knapsack.Usergame'),
        ),
    ]