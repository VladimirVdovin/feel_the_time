from django.contrib import admin
from.models import Time, Activities



class TimeAdmin(admin.ModelAdmin):
    list_display = ['name', 'current_activity', 'time', 'duration']

class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ['activity_name', 'activity_rank']

admin.site.register(Time, TimeAdmin)
admin.site.register(Activities)