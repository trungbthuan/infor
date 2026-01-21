from django.contrib import admin
from django.urls import path, include
from . import views as testUrl_views

urlpatterns = [
    path('home/', testUrl_views.call_home, name='home'),
    path('main/', testUrl_views.call_main, name='main'),
    path('temp/', testUrl_views.call_temp, name='temp'),
    path('temp2/', testUrl_views.call_temp2, name='temp2'),
    path('students/', testUrl_views.get_students, name='students'),
]