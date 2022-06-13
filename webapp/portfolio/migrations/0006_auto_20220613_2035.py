# Generated by Django 3.2.2 on 2022-06-13 18:35

import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models

import webapp.portfolio.validators


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_alter_customuser_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, error_messages={'unique': 'A user with that phone number already exists.'}, max_length=50, null=True, region=None, unique=True, validators=[webapp.portfolio.validators.phone_number_validator]),
        ),
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.DateTimeField(auto_now_add=True)),
                ('logout', models.DateTimeField(default=None, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user activity',
                'verbose_name_plural': 'user activities',
                'default_manager_name': 'objects',
            },
        ),
    ]
