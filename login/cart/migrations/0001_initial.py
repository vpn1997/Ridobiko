# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 21:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bike_name', models.CharField(db_column='Bike_Name', max_length=15)),
                ('image', models.CharField(db_column='Image', max_length=15)),
                ('price', models.IntegerField()),
            ],
            options={
                'db_table': 'cart',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('vendor', models.CharField(db_column='Vendor', max_length=15, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'seller',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Bikes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=15)),
                ('bike_status', models.IntegerField()),
            ],
        ),
    ]