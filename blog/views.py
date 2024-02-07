from typing import Any
from django import contrib
from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View

from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
)

from .utils import handle_uploaded_file

from .forms import BlogForm, BlogModelForm, UploadForm
from .models import Blog, Category, Tags, UploadFiles
from django.db.models import Q, Count
from django.views.decorators.csrf import csrf_exempt


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.decorators.cache import cache_page
# Create your views here.


def home_view(request):
    return render(request, "blog/home.html")


class HomePage(TemplateView):
    template_name = "blog/home.html"


# @csrf_exempt
@login_required  # (login_url="/admin")
def add_blog_view(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            try:
                Blog.objects.create(**form.cleaned_data)
                return redirect("blogs")
            except Exception as e:
                print("Error creating:", e)
                form.add_error(None, "Cannot add a new blog")
            print(form.cleaned_data)
    else:
        form = BlogForm()

    context = {
        "title": "Добавить новый Блог",
        "form": form,
    }
    return render(request, "blog/add.html", context)


def add_model_blog_view(request):
    if request.method == "POST":
        form = BlogModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            return redirect("blogs")
    else:
        form = BlogModelForm()

    context = {
        "title": "Добавить новый Блог",
        "form": form,
    }
    return render(request, "blog/add.html", context)


class AddFormPage(FormView):
    form_class = BlogModelForm
    template_name = "blog/add.html"
    # success_url = reverse('blogs')
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AddCreateFormPage(LoginRequiredMixin, CreateView):
    model = Blog
    fields = "__all__"
    # ["title","slug","content","author","category"]
    # form_class = BlogModelForm
    template_name = "blog/add.html"
    # success_url = reverse('blogs')
    # success_url = reverse_lazy('blogs') #
    # get_absolute_url

    # def form_valid(self, form):
    #     blog = form.save(commit = False)
    #     blog.author = self.request.user

    #     return super().form_valid(form)


class UpdateFormPage(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = "__all__"
    # form_class = BlogModelForm
    template_name = "blog/add.html"
    # success_url = reverse('blogs')
    # success_url = reverse_lazy('blogs') # get_absolute_url


class AddPage(View):
    def get(self, request):
        form = BlogModelForm()
        context = {
            "title": "Добавить новый Блог",
            "form": form,
        }
        return render(request, "blog/add.html", context)

    def post(self, request):
        form = BlogModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            return redirect("blogs")

        # context = {
        #     "title": "Добавить новый Блог",
        #     "form": form,
        # }
        # return render(request, "blog/add.html", context)


def upload_image_view(request):
    if request.method == "POST":
        print(request.FILES)
        handle_uploaded_file(request.FILES["profile_image"])

    context = {}
    return render(request, "blog/upload.html", context)


def upload_image_using_form_view(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = UploadFiles(image=form.cleaned_data["file"])
            file.save()
    else:
        form = UploadForm()

    context = {"form": form, "title": "Загрузка файлов"}
    return render(request, "blog/upload.html", context)


@login_required
# @cache_page(5)
def blogs_view(request):
    blogs = (
        Blog.objects.all().select_related("author", "category").prefetch_related("tags")
    )

    paginator = Paginator(blogs, 10)

    page_number = request.GET.get("page")

    page = paginator.get_page(page_number)

    pagination = paginator.get_elided_page_range(page.number, on_each_side=3, on_ends=2)
    """
    # try:
    #     page = paginator.page(page_number)
    # except EmptyPage as e:
    #     page = paginator.page(1)
    # except PageNotAnInteger as e:
    #     page = paginator.page(1)
    
    # p1.start_index()
    # page = "sadsad"
    """
    context = {
        "title": "Блоги",
        "posts": page,
        "pagination": list(pagination),
        "page": page,
        "paginator": paginator,
    }

    return render(request, "blog/blogs.html", context)


class BlogsPage(ListView):
    # model = Blog
    template_name = "blog/blogs.html"
    context_object_name = "posts"  # по умолчанию стоит object_list
    allow_out_of_range = True
    queryset = (
        Blog.objects.all().select_related("author", "category").prefetch_related("tags")
    )
    extra_context = {
        "title": "Блоги",
    }

    paginate_by = 5
    page_kwarg = "page"  # По умолчанию "page"

    def paginate_queryset(self, queryset, page_size):
        paginator = Paginator(queryset, page_size)
        page_number = self.kwargs.get("page") or self.request.GET.get("page") or 1
        page = paginator.get_page(page_number)

        return (paginator, page, page.object_list, paginator.count)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add extra context if needed
        context["title"] = "Блоги"
        paginator = context["paginator"]
        page = context["page_obj"]
        context["page"] = context["page_obj"]

        pagination = paginator.get_elided_page_range(
            page.number, on_each_side=3, on_ends=2
        )
        context["pagination"] = list(pagination)
        return context


def author_slug_view(request, author_slug):
    blogs = (
        Blog.objects.filter(author__slug=author_slug)
        .select_related("author", "category")
        .prefetch_related("tags")
    )
    context = {"title": f"Автор: {blogs.distinct('author')[0].author}", "posts": blogs}
    return render(request, "blog/blogs.html", context)


def search_view(request):
    query = request.GET.get("q")
    blogs = (
        Blog.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        .select_related("author", "category").prefetch_related("tags")
    )
    context = {
        "title": f"Search {query}",
        "results": len(blogs),
        "posts": blogs,
        "query": query,
    }

    return render(request, "blog/search.html", context)


def blog_slug_view(request, blog_slug):
    blog = Blog.objects.get(slug=blog_slug)
    context = {"title": f"Блог: {blog.title}", "post": blog}
    return render(request, "blog/blog.html", context)


class BlogSlugPage(DetailView):
    # model = Blog.objects.get(slug = slug_url_kwarg, is_published = True)
    template_name = "blog/blog.html"
    slug_url_kwarg = "blog_slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Блог: {context['post'].title}"
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(
            Blog, slug=self.kwargs[self.slug_url_kwarg]
            # , is_published=True
        )


def category_slug_view(request, category_slug):
    blogs = Blog.objects.filter(category__slug=category_slug).select_related(
        "author", "category"
    )
    context = {
        "title": f"Категория: {blogs.distinct('category')[0].category}",
        "posts": blogs,
    }
    return render(request, "blog/blogs.html", context)


class CategorySlugPage(ListView):
    template_name = "blog/blogs.html"
    context_object_name = "posts"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs["category_slug"])
        context["title"] = f"Категория: {category}"
        return context

    def get_queryset(self):
        return (
            Blog.objects.filter(category__slug=self.kwargs["category_slug"])
            .select_related("author", "category")
            .prefetch_related("tags")
        )


def tag_slug_view(request, tag_slug):
    blogs = (
        Blog.objects.filter(tags__slug=tag_slug)
        .select_related("author", "category")
        .prefetch_related("tags")
    )
    tag = Tags.objects.get(slug=tag_slug)
    context = {
        "title": f"Тег: {tag.tag_name}",
        "posts": blogs,
    }
    return render(request, "blog/blogs.html", context)


def handler_view_404(request, exception):
    return render(request, "blog/page404.html")


def handler_view_500(request):
    return render(request, "blog/page500.html")