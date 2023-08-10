from django.db import models
from datetime import timedelta

class Activities(models.Model):
    activity_name = models.CharField(max_length=30, null=True)
    activity_rank = models.CharField(max_length=30, null=True)
    total_time = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.activity_name} ({self.activity_rank})'

class Time(models.Model):
    name = models.CharField(max_length=30, null=True)
    current_activity = models.ForeignKey(Activities, on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField()
    duration = models.DurationField(default=timedelta(seconds=0))

class Buttons(models.Model):
    pass

class Person(models.Model):
    pass




