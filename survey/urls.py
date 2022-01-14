from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('<int:pk>/', index, name='index'),
    path('result/', result, name='result'),
]
