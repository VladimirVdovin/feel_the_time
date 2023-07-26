from django.db import models

class Activities(models.Model):
    activity_name = models.CharField(max_length=30, null=True)
    activity_rank = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f'{self.activity_name} ({self.activity_rank})'

class Time(models.Model):
    name = models.CharField(max_length=30, null=True)
    current_activity = models.ForeignKey(Activities, on_delete=models.PROTECT, null=True)
    time = models.DateTimeField()
    duration = models.IntegerField(default=0)


