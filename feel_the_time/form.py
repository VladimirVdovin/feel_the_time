from django import forms
from .models import Person

class PersonalButtonsForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['button_set', 'rank_set']
        labels = {
                'button_set': 'Добавьте кпопку',
                'rank_set': 'Какой у нее статус'
        }