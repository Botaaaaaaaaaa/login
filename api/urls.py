from django.urls import path
from . import views

urlpatterns = [
    path("blog_list/",views.BlogApiView.as_view(),name="blog_list"),
]
