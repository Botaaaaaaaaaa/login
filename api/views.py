from django.shortcuts import render
from rest_framework import generics
from blog.models import Blog
from .serializers import BlogSerializer
# Create your views here.

class BlogApiView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer