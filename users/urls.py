from django.urls import path

from . import views
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns = [
 
    path("login/", views.LoginPage.as_view(), name="login"),
   
    path("logout/", LogoutView.as_view(), name="logout"),
 
    path("register/", views.RegisterPage.as_view(), name="register"),
    path("profile/", views.UserProfilePage.as_view(), name="profile"),
    path(
        "change_password/", views.ChangePasswordPage.as_view(), name="change_password"
    ),
    path(
        "change_password_done/",
        PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),
        name="password_change_done",
    ),
    path("reset_password/", 
        PasswordResetView.as_view(
            template_name = "users/password_reset.html"
        ), 
        name="password_reset"),
    path(
        "reset_password_done/",
        PasswordResetDoneView.as_view(
            template_name = "users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset_password/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name = "users/password_reset_confirm.html"    
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        PasswordResetCompleteView.as_view(
            template_name = "users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]