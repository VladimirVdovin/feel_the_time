from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Time, Activities, Person
from .forms import PersonalButtonsForm, RegistrationForm, AuthForm
from django.db.models import Sum
from matplotlib import pyplot as plt
from io import BytesIO
import base64
from datetime import timedelta, datetime
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
import random
from tzlocal import get_localzone
import pytz


def get_user_or_create_temporary_user(request):
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
    return user


def setting_the_day_border(penultimate_activity, current_time, user):
    server_timezone = get_localzone()
    midnight = current_time.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=server_timezone)
    uts_timezone = pytz.timezone('UTC')
    midnight_utc = midnight.astimezone(uts_timezone)
    before_midnight = midnight_utc - penultimate_activity.time
    after_midnight = current_time - midnight_utc
    penultimate_activity.duration = before_midnight
    penultimate_activity.save()
    Time.objects.create(name=user, time=midnight, current_activity=penultimate_activity.current_activity,
                        duration=after_midnight)


def button(request):
    user = get_user_or_create_temporary_user(request)
    person, created = Person.objects.get_or_create(user_name=user)

    if request.method == 'POST': 
        button_value = request.POST.get('button_click')
        current_time = timezone.now()

        if Time.objects.count() != 0:
            penultimate_activity = Time.objects.last()
            penultimate_activity.duration = current_time - penultimate_activity.time
            penultimate_activity.save()

        if timezone.now().day != penultimate_activity.time.day:
            setting_the_day_border(penultimate_activity, current_time, user)

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

        form = PersonalButtonsForm()
        content = {
            'form': form,
            'person': person,
            }
        return render(request, 'feel_the_time/buttons.html', context=content)

    def post(self, request):
        if 'button_set_form' in request.POST:
            checkbox_set = request.POST.getlist("checkbox_set")
            buttons_change = Person.objects.get(user_name=request.user)
            buttons_change.actual_button_set = checkbox_set
            buttons_change.save()
            return HttpResponse(buttons_change.actual_button_set)

        elif 'add_button_form' in request.POST:
            person = Person.objects.get(user_name=request.user)

            old_buttons = person.actual_button_set or []
            all_buttons = person.all_personal_buttons or []
            old_ranks = person.actual_rank_set or []
            all_ranks = person.all_personal_ranks or []

            form = PersonalButtonsForm(request.POST, instance=person)
            if form.is_valid():
                instance = form.save(commit=False)

                new_button = request.POST.getlist('actual_button_set')
                new_rank = request.POST.getlist('actual_rank_set')

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


            return render(request, 'feel_the_time/buttons.html', context={'form': form,
                                                                          'person': person,
                                                                          })

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












