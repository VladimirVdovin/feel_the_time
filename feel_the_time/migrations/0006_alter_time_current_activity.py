# Generated by Django 4.2.1 on 2023-08-31 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feel_the_time', '0005_alter_person_actual_rank_set_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='time',
            name='current_activity',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
