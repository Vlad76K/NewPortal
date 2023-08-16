# Generated by Django 4.2.3 on 2023-08-11 19:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newsportalapp', '0005_appointment'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscribeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Subscribers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribers', models.ManyToManyField(through='newsportalapp.SubscribeCategory', to='newsportalapp.category')),
                ('subscribers_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='subscribecategory',
            name='author_connection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsportalapp.subscribers'),
        ),
        migrations.AddField(
            model_name='subscribecategory',
            name='category_connection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsportalapp.category'),
        ),
    ]