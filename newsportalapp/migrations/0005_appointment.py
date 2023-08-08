# Generated by Django 4.2.3 on 2023-08-08 17:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsportalapp', '0004_authorcategory_author_author_subscribers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.utcnow)),
                ('client_name', models.CharField(max_length=200)),
                ('message', models.TextField()),
            ],
        ),
    ]
