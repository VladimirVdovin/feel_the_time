from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Time, Activities, Person
from .forms import PersonalButtonsForm, RegistrationForm, AuthForm
from django.db.models import Sum
from matplotlib import pyplot as plt
from io import BytesIO
import base64
from datetime import timedelta
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
import random



def button(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        if not request.session.get('temporary_user'):
            username = 'User' + str(random.random())
            user = User.objects.create_user(username=username, password='')
            request.session['temporary_user'] = user.username
            session = request.session
            session.set_expiry(3600)
        else:
            username = request.session['temporary_user']
            user = User.objects.get(username=username)
    person, created = Person.objects.get_or_create(user_name=user)

    if request.method == 'POST': 
        button_value = request.POST.get('button_click')
        current_time = timezone.now()

        if Time.objects.count() != 0:
            penultimate_activity = Time.objects.last()
            penultimate_activity.duration = current_time - penultimate_activity.time
            penultimate_activity.save()

        Time.objects.create(name=user, time=current_time, current_activity=button_value)
        current_activity = Time.objects.filter(name=user).order_by('-time')[0]
        all_activities = Time.objects.filter(name=user).order_by('-time')[1:]

        data = {'current_activity': current_activity,
                'all': all_activities,
                'person': person,
                }
        return render(request, 'feel_the_time/main.html', context=data)
    else:

        all_activities = Time.objects.filter(name=user).order_by('-time')[1:]
        data = {'all': all_activities,
                'person': person,
                }
        return render(request, 'feel_the_time/main.html', context=data)


def graph(request, period: str):

    if not request.user.is_authenticated and not request.session.get('temporary_user'):
        return redirect('main_page')
    else:

        total_time = []
        activities = Person.objects.get(user_name=request.user).actual_button_set
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

        # activities_names = [act.activity_name for act in activities]

        plt.figure(figsize=(9, 5))
        plt.barh(activities, total_time)
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
        person = Person.objects.get(user_name=request.user)
        # all_activities = Activities.objects.values_list('activity_name', flat=True)
        form = PersonalButtonsForm()
        content = {
            'form': form,
            'person': person,
            # 'all_buttons': all_activities
            }
        return render(request, 'feel_the_time/buttons.html', context=content)

    def post(self, request):
        if 'button_set_form' in request.POST:
            checkbox_set = request.POST.getlist("checkbox_set")
            buttons_change = Person.objects.get(user_name=request.user.username)
            buttons_change.actual_button_set = checkbox_set
            buttons_change.save()
            return HttpResponse(buttons_change.actual_button_set)

        elif 'add_button_form' in request.POST:
            person = Person.objects.get(user_name=request.user.username)
            old_buttons = person.actual_button_set or []
            all_buttons = person.all_personal_buttons or []
            old_ranks = person.actual_rank_set or []
            all_ranks = person.all_personal_ranks or []
            form = PersonalButtonsForm(request.POST, instance=person)
            if form.is_valid():
                instance = form.save(commit=False)
                # Activities.objects.create(activity_name=instance.actual_button_set[0], activity_rank=instance.actual_rank_set[0])
                new_button = request.POST.getlist('button_set')
                new_rank = request.POST.getlist('rank_set')

                old_buttons.extend(new_button)
                old_ranks.extend(new_rank)
                all_buttons.extend(new_button)
                all_ranks.extend(new_rank)

                instance.actual_button_set = old_buttons
                instance.actual_rank_set = old_ranks
                instance.all_personal_buttons = old_buttons
                instance.all_personal_ranks = old_ranks

                instance.save()
                form = PersonalButtonsForm()
                all_activities = Activities.objects.values_list('activity_name', flat=True)

            return render(request, 'feel_the_time/buttons.html', context={'form': form,
                                                                          'personal_buttons': person,
                                                                          'all_buttons': all_activities})

def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main_page')
    else:
        form = RegistrationForm()
    return render(request, 'feel_the_time/registration.html', context={'form': form})

def authorization(request):
    if request.method == "POST":
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main_page')
    else:
        form = AuthForm()
    return render(request, 'feel_the_time/authorization.html', context={'form': form})

def about(request):
    return HttpResponse('<h1>Здесь будет информация о программе</h1>')



# from django.contrib.sessions.models import Session

# def button(request):
#     if request.method == 'POST':
#         # Обработка POST-запроса
#     else:
#         if request.user.is_authenticated:
#             user = request.user
#         else:
#             if not request.session.get('temporary_user'):
#                 # Если у пользователя нет временного имени, создаем его
#                 username = 'User' + str(random.random())
#                 user = User.objects.create_user(username=username, password='')
#                 request.session['temporary_user'] = user.username
#             else:
#                 # Если у пользователя уже есть временное имя, используем его
#                 username = request.session['temporary_user']
#                 user = User.objects.get(username=username)
#
#         person, created = Person.objects.get_or_create(user_name=user)
#         all_activities = Time.objects.filter(name=user).order_by('-time')

# # Получение объекта сессии
# session = request.session
#
# # Установка срока действия сессии для этой конкретной сессии в секундах
# # Например, установим срок действия данной сессии в 1 час (3600 секунд)
# session.set_expiry(3600)









