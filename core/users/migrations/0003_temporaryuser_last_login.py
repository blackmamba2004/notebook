# Generated by Django 4.2.9 on 2024-08-27 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_temporaryuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='temporaryuser',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
    ]
