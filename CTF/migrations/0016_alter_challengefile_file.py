# Generated by Django 5.2 on 2025-06-29 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CTF', '0015_customeuser_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challengefile',
            name='file',
            field=models.FileField(upload_to='challenges/'),
        ),
    ]
