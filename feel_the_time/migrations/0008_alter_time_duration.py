# Generated by Django 4.2.1 on 2023-07-16 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feel_the_time', '0007_alter_time_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='time',
            name='duration',
            field=models.DateTimeField(null=True),
        ),
    ]
