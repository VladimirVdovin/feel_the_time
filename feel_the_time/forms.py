from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Person

class PersonalButtonsForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['actual_button_set', 'actual_rank_set']
        labels = {
                'actual_button_set': 'Добавьте кпопку',
                'actual_rank_set': 'Какой у нее статус'
        }

class RegistrationForm(UserCreationForm):
    pass

class AuthForm(AuthenticationForm):
    pass

