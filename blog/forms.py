from dataclasses import fields
from django import forms

from .models import Author, Blog, Category, Tags


class BlogForm(forms.Form):
    title = forms.CharField(max_length=100, label="Заголовок")
    slug = forms.SlugField(max_length=100, label="URL slug")
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": "5"}))
    is_published = forms.BooleanField(initial=True, required=False)  # Rquired

    author = forms.ModelChoiceField(
        queryset=Author.objects.all(), empty_label="Автор не выбран"
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label="Категория не выбрана"
    )
    # tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all())


class BlogModelForm(forms.ModelForm):
    # author = forms.ModelChoiceField(queryset=Author.objects.all(), empty_label="Автор не выбран")
    # category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label = "Категория не выбрана")
    # tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all())

    class Meta:
        model = Blog
        fields = [
            "title",
            "slug",
            "content",
            "author",
            "category",
            "is_published",
            "image",
        ]
        # fields = "__all__"


class UploadForm(forms.Form):
    file = forms.ImageField()