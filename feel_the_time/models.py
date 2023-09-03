from django.db import models
from datetime import timedelta
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User


class Activities(models.Model):
    activity_name = models.CharField(max_length=15, null=True)
    activity_rank = models.CharField(max_length=15, null=True)
    total_time = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.activity_name} - {self.activity_rank}'


def default_button_set():
    return ['Работа', 'Семья', 'Готовить', 'Спорт', 'В пути', 'Ванна', 'Отдых', 'Есть, пить', 'Уборка', 'Сон']

def default_rank_set():
    return ['Необходимо', 'Важно', 'Не важно', 'Важно', 'Не важно', 'Не важно', 'Не важно', 'Необходимо',
            'Не важно', 'Необходимо']

class Person(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    actual_button_set = ArrayField(models.CharField(max_length=100), default=default_button_set, null=True)
    actual_rank_set = ArrayField(models.CharField(max_length=100), default=default_rank_set, null=True)
    all_personal_buttons = ArrayField(models.CharField(max_length=100), default=default_button_set, null=True)
    all_personal_ranks = ArrayField(models.CharField(max_length=100), default=default_rank_set, null=True)

    def __str__(self):
        return f'{self.user_name.username} - {self.actual_button_set} - {self.actual_rank_set}'


class Time(models.Model):
    name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    current_activity = models.CharField(max_length=15, null=True)
    time = models.DateTimeField()
    duration = models.DurationField(default=timedelta(seconds=0))
    comment = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f'{self.name} - {self.current_activity} - {self.time} - {self.duration} - {self.comment}'







