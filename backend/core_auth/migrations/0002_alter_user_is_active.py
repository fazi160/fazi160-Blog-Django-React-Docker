# Generated by Django 5.0.1 on 2024-01-16 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]