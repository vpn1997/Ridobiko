# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 21:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bikes',
        ),
    ]