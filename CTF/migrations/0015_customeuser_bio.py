# Generated by Django 5.2 on 2025-06-27 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CTF', '0014_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeuser',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
