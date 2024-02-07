from django.db import models
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model


class Tags(models.Model):
    tag_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.tag_name

    def get_absolute_url(self):
        return reverse("tag_slug", kwargs={"tag_slug": self.slug})

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок Статьи")
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)

    image = models.ImageField(
        upload_to="blog_images", null=True, blank=True, default=None
    )

    category = models.ForeignKey(
        "Category", on_delete=models.PROTECT, related_name="category_blogs"
    )
    author = models.ForeignKey(
        "Author", on_delete=models.PROTECT, related_name="author_blogs"
    )
    
    tags = models.ManyToManyField("Tags", related_name="tag_blogs")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy("blog_slug", kwargs={"blog_slug": self.slug})

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"
        ordering = ["id"]


class Author(models.Model):
    author_name = models.CharField(max_length=100),
    email = models.EmailField()
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)

    def __str__(self):
        return self.author_name

    def get_absolute_url(self):
        return reverse("author_slug", kwargs={"author_slug": self.slug})

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse("category_slug", kwargs={"category_slug": self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class UploadFiles(models.Model):
    image = models.ImageField(upload_to="blog_images")