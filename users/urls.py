from django.shortcuts import render
from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('register/', views.registerView, name='register'),
    path('special/', views.special, name='special'),
    path('profile/', views.user_profile, name='profile'),
]