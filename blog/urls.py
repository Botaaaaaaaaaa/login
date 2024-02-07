from django.urls import path

from . import views
from django.views.decorators.cache import cache_page 

urlpatterns = [
    # HOME
    path("", views.home_view, name="home"),
    # SEARCH
    path("search/", views.search_view, name="search"),
    # BLOG
    path("add_blog/", views.add_blog_view, name="add_blog"),
    path("add_model_blog/", views.add_model_blog_view, name="add_model_blog"),
    path("blogs/", views.blogs_view, name="blogs"),
    # path("blog/<slug:blog_slug>", views.blog_slug_view, name="blog_slug"),
    # AUTHOR
    path("author/<slug:author_slug>", views.author_slug_view, name="author_slug"),
    # TAGS
    path("tag/<slug:tag_slug>", views.tag_slug_view, name="tag_slug"),
    # CATEGORY
    # path(
    #     "category/<slug:category_slug>", views.category_slug_view, name="category_slug"
    # ),
    # TEST
    path("upload_image/", views.upload_image_view, name="upload_image"),
    path(
        "upload_form_image/",
        views.upload_image_using_form_view,
        name="upload_form_image",
    ),
    # CBV
    path("home/", views.HomePage.as_view(), name="home_cbv"),
    path("add_blog_cbv/", views.AddPage.as_view(), name="add_model_blog_cbv"),
    path("blogs_cbv/", cache_page(10)(views.BlogsPage.as_view()), name="blogs_cbv"),
    path(
        "category/<slug:category_slug>",
        views.CategorySlugPage.as_view(),
        name="category_slug",
    ),
    path("blog/<slug:blog_slug>", views.BlogSlugPage.as_view(), name="blog_slug"),
    path(
        "add_model_form_blog/", views.AddFormPage.as_view(), name="add_model_form_blog"
    ),
    path(
        "add_model_create_form_blog/",
        views.AddCreateFormPage.as_view(),
        name="add_model_create_form_blog",
    ),
    path(
        "update_model_form_blog/<slug:slug>",
        views.UpdateFormPage.as_view(),
        name="update_model_form_blog",
    ),
]