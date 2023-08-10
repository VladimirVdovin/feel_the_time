from django.urls import path
from .views import button, graph, buttons_set

urlpatterns = [
    path('', button, name='main_page'),
    path('graph/<str:period>', graph, name='graph'),
    path('buttons', buttons_set, name='buttons_set'),
]
