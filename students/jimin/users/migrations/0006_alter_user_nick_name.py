# Generated by Django 4.0.5 on 2022-06-16 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_nick_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nick_name',
            field=models.CharField(max_length=45, unique=True),
        ),
    ]
