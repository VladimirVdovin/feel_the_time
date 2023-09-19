from django.contrib import admin
from.models import Time, Person

admin.site.register(Time)
admin.site.register(Person)

class TimeAdmin(admin.ModelAdmin):
    list_display = ['name', 'time', 'duration']

class PersonAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'button_set', 'rank_set']

