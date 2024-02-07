from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy

from .forms import LoginForm, RegisterForm, UserPasswordChangeForm, UserProfileForm
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import get_user_model


# Create your views here.
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data["login"], password=data["password"]
            )

            if user and user.is_active:
                login(request, user)
                return redirect("home")
    else:
        form = LoginForm()

    context = {
        "title": "Авторизация",
        "form": form,
    }
    return render(request, "users/login.html", context)


class LoginPage(LoginView):
    form_class = LoginForm
    template_name = "users/login.html"

    extra_context = {
        "title": "Авторизация",
    }

    # def get_success_url(self):
    #     return reverse_lazy('blogs')


# def logout_view(request):
#     logout(request)
#     return redirect('login')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("login")
    else:
        form = RegisterForm()

    context = {
        "title": "Регистрация",
        "form": form,
    }
    return render(request, "users/register.html", context)


class RegisterPage(CreateView):
    form_class = RegisterForm
    template_name = "users/register.html"
    extra_context = {
        "title": "Регистрация",
    }

    success_url = reverse_lazy("login")


class UserProfilePage(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserProfileForm
    template_name = "users/profile.html"
    extra_context = {
        "title": "Профиль",
    }
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user


class ChangePasswordPage(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = "users/password_change.html"
    success_url = reverse_lazy("password_change_done")