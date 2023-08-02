from django.urls import path
from .views import button, graph

urlpatterns = [
    path('', button, name='main_page'),
    path('graph', graph, name='graph'),

]
