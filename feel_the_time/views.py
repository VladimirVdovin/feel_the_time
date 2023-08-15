from django.shortcuts import render
from django.utils import timezone
from .models import Time, Activities, Person
from .form import PersonalButtonsForm
from django.db.models import Sum
from matplotlib import pyplot as plt
from io import BytesIO
import base64
from datetime import timedelta
from django.views import View
from django.http import HttpResponse


buttons = ['Работа', 'Семья', 'Готовить', 'Спорт', 'В пути', 'Ванна', 'Отдых', 'Уборка', 'Есть, пить']


def button(request):
    if request.method == 'POST':
        button_value = request.POST.get('button_click')
        current_time = timezone.now()

        if Time.objects.count() != 0:
            penultimate_activity = Time.objects.last()
            penultimate_activity.duration = current_time - penultimate_activity.time
            penultimate_activity.save()

        activity = Activities.objects.get_or_create(activity_name=button_value)
        person = Person.objects.get_or_create(user_name='Vladimir')
        Time.objects.create(name=person[0], time=current_time, current_activity=activity[0])
        current_activity = Time.objects.order_by('-time')[0]
        all_activities = Time.objects.order_by('-time')[1:]

        data = {'current_activity': current_activity,
                'all': all_activities,
                'buttons': buttons,
                }
        return render(request, 'feel_the_time/main.html', context=data)
    else:

        all_activities = Time.objects.order_by('-time')[1:]
        data = {'all': all_activities,
                'buttons': buttons,
                }
        return render(request, 'feel_the_time/main.html', context=data)


def graph(request, period: str):

    total_time = []
    activities = Activities.objects.all()
    now = timezone.now()
    current_time = now.replace(hour=0, minute=0, second=0, microsecond=0)

    if period == "day":
        for obj in activities:
            sum_result = Time.objects.filter(current_activity=obj, time__day=current_time.day).aggregate(Sum('duration'))
            total_time.append((sum_result['duration__sum'] or timedelta(seconds=0)).total_seconds())


    elif period == 'week':
        current_weekday = current_time.weekday()
        start_of_week = current_time - timedelta(days=current_weekday)
        for obj in activities:
            sum_result = Time.objects.filter(current_activity=obj, time__day__gte=start_of_week.day).aggregate(Sum('duration'))
            total_time.append((sum_result['duration__sum'] or timedelta(seconds=0)).total_seconds())

    elif period == 'month':
        current_monthday = current_time.day
        start_of_month = current_time - timedelta(days=current_monthday-1)
        for obj in activities:
            sum_result = Time.objects.filter(current_activity=obj, time__day__gte=start_of_month.day).aggregate(Sum('duration'))
            total_time.append((sum_result['duration__sum'] or timedelta(seconds=0)).total_seconds())

    activities_names = [act.activity_name for act in activities]

    plt.figure(figsize=(9, 5))
    plt.barh(activities_names, total_time)
    max_time = max(total_time)
    x_limit = max_time * 1.3

    plt.xlabel('Время')
    plt.ylabel('Активность')
    plt.title('Затраченное время')
    plt.xlim(0, x_limit)

    for i, time in enumerate(total_time):
        plt.annotate(f'{int(time//3600)} ч {int((time % 3600)//60)} мин', (time, i), textcoords="offset points",
                     xytext=(35, 0), ha='center', fontsize=10)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()

    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return render(request, 'feel_the_time/graph.html', context={'graphic': graphic, 'period': period})

class ButtonSetView(View):
    def get(self, request):
        form = PersonalButtonsForm()
        return render(request, 'feel_the_time/buttons.html', context={'form': form})

    def post(self, request):
        form = PersonalButtonsForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'feel_the_time/buttons.html', context={'form': form})





