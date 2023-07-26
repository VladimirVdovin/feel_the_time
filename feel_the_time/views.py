from django.shortcuts import render
from django.utils import timezone
from .models import Time, Activities
from django.db.models import Sum

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

        # work_time = Time.objects.filter(activity='Работа').aggregate(Sum('duration'))
        # family_time = Time.objects.filter(activity='Семья').aggregate(Sum('duration'))
        # cooking_time = Time.objects.filter(activity='Готовить').aggregate(Sum('duration'))

        data = {'current_activity': current_activity,
                'all': all_activities,
                'difference_in_sec': difference_in_sec,
                # 'work_time': work_time['duration__sum'],
                # 'family_time': family_time['duration__sum'],
                # 'cooking_time': cooking_time['duration__sum'],
                'buttons': buttons
                }
        return render(request, 'feel_the_time/main.html', context=data)
    else:

        all_activities = Time.objects.order_by('-time')[1:]
        data = {'all': all_activities,
                'buttons': buttons
                }
        return render(request, 'feel_the_time/main.html', context=data)




