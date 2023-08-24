from django.urls import path
from .views import button, graph, ButtonSetView, registration, authorization, about

urlpatterns = [
    path('', button, name='main_page'),
    path('graph/<str:period>', graph, name='graph'),
    path('buttons', ButtonSetView.as_view(), name='buttons_set'),
    path('registration', registration, name='registration'),
    path('authorization', authorization, name='authorization'),
    path('about', about, name='about')
]
