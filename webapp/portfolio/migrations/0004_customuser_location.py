# Generated by Django 3.2.2 on 2022-06-12 19:08

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(default=None, srid=4326),
        ),
    ]