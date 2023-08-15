from django.db import models
from datetime import timedelta
from django.contrib.postgres.fields import ArrayField

class Activities(models.Model):
    activity_name = models.CharField(max_length=15, null=True)
    activity_rank = models.CharField(max_length=15, null=True)
    total_time = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.activity_name} - {self.activity_rank}'

class Person(models.Model):
    user_name = models.CharField(max_length=15, null=True)
    button_set = ArrayField(models.CharField(max_length=15), null=True)
    rank_set = ArrayField(models.CharField(max_length=15), null=True)

    def __str__(self):
        return f'{self.user_name} - {self.button_set} - {self.button_set}'


class Time(models.Model):
    name = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)
    current_activity = models.ForeignKey(Activities, on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField()
    duration = models.DurationField(default=timedelta(seconds=0))
    comment = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f'{self.name} - {self.current_activity} - {self.time} - {self.duration} - {self.comment}'







