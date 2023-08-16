from django.contrib import admin
from.models import Time, Activities, Person

admin.site.register(Time)
admin.site.register(Activities)
admin.site.register(Person)

class TimeAdmin(admin.ModelAdmin):
    list_display = ['name', 'time', 'duration']

class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ['activity_name', 'activity_rank']

class PersonAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'button_set', 'rank_set']

