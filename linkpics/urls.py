from django.contrib import admin
from django.urls import path

# from .views import index
from .views import index, about

urlpatterns = [
    path("", index),
    # path("about/",about),
]