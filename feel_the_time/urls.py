from django.urls import path
from .views import button, graph, ButtonSetView

urlpatterns = [
    path('', button, name='main_page'),
    path('graph/<str:period>', graph, name='graph'),
    path('buttons', ButtonSetView.as_view(), name='buttons_set'),
]
