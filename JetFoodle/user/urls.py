from django.contrib import admin
from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('Register/', views.Register.as_view(), name="register"),
    path('login/', views.LoginUser.as_view(), name="login"),
    path('logout/', views.LogoutUser.as_view(), name="logout"),
]

