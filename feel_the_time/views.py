from django.shortcuts import render
from django.utils import timezone
from .models import Time, Activities
from django.db.models import Sum
from matplotlib import pyplot as plt
from io import BytesIO
import base64


buttons = ['Работа', 'Семья', 'Готовить', 'Спорт', 'В пути', 'Ванна', 'Отдых', 'Уборка', 'Есть, пить']

def button(request):
    if request.method == 'POST':
        button_value = request.POST.get('button_click')
        current_time = timezone.now()

        penultimate_activity = Time.objects.order_by('-id')[0]
        difference = current_time - penultimate_activity.time
        difference_in_sec = difference.total_seconds()
        penultimate_activity.duration = difference_in_sec
        penultimate_activity.save()

        activity = Activities.objects.get_or_create(activity_name=button_value)
        Time.objects.create(name='Vladimir', time=current_time, current_activity=activity[0])
        current_activity = Time.objects.order_by('-time')[0]
        all_activities = Time.objects.order_by('-time')[1:]

        data = {'current_activity': current_activity,
                'all': all_activities,
                'difference_in_sec': difference_in_sec,
                'buttons': buttons,
                'graphic': grath()
                }
        return render(request, 'feel_the_time/main.html', context=data)
    else:

        all_activities = Time.objects.order_by('-time')[1:]
        data = {'all': all_activities,
                'buttons': buttons
                }
        return render(request, 'feel_the_time/main.html', context=data)

def grath():

    total_time = []
    activities = Activities.objects.all()
    for obj in activities:
        sum_result = Time.objects.filter(current_activity=obj).aggregate(Sum('duration'))
        total_time.append(sum_result['duration__sum'])


    acts = Activities.objects.all()
    names = [act.activity_name for act in acts]

    plt.figure(figsize=(10, 6))
    plt.barh(names, total_time)
    plt.xlabel('Время')
    plt.ylabel('Активность')
    plt.title('Затраченное время')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()

    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic
