# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-20 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_q', '0006_course_sign_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='student_num',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
