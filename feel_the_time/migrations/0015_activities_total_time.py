# Generated by Django 4.2.1 on 2023-07-27 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feel_the_time', '0014_activities_remove_time_activity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activities',
            name='total_time',
            field=models.IntegerField(default=0),
        ),
    ]
