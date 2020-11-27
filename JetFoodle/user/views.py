from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views import View


class Register(View):

    @staticmethod
    def get(request, *args, **kwargs):
        form = RegisterForm
        return render(request, "register.html", {"form": form})

    @staticmethod
    def post(request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            new_user = User(username=username)
            new_user.set_password(password)
            new_user.save()
            login(request, new_user)
            messages.success(request, "Başarıyla Kayıt Oldunuz...")
            return redirect("index")

        else:
            return render(request, "register.html", {"form": form})


class LoginUser(View):

    @staticmethod
    def get(request, *args, **kwargs):
        form = LoginForm
        return render(request, "login.html", {"form": form})

    @staticmethod
    def post(request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is None:
                messages.warning(request, 'Kullanıcı Adı veya Parola Hatalı...')
                return render(request, "login.html", {"form": form})

            else:
                #messages.success(request, "Başarıyla Giriş Yaptınız...")
                login(request, user)
                return redirect("index")


class LogoutUser(View):

    @staticmethod
    def get(request):
        logout(request)
        messages.success(request, "Başarıyla Çıkış Yaptınız..")
        return redirect("index")



