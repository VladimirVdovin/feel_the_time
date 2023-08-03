from django.urls import path
from .views import button, graph, just_try

urlpatterns = [
    path('', button, name='main_page'),
    path('graph', graph, name='graph'),
    path('just_try', just_try, name='just_try'),

]
