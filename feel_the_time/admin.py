from django.contrib import admin
from.models import Time, Activities



class TimeAdmin(admin.ModelAdmin):
    list_display = ['name', 'time', 'duration']

class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ['activity_name', 'activity_rank']

admin.site.register(Time, TimeAdmin)
admin.site.register(Activities)