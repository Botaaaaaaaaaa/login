# from django.contrib import admin, messages
# from .models import Blog, Author
# from django.contrib import admin, messages
# from .models import Blog, Author, Category, Tags
# from django.utils.safestring import mark_safe

# # Register your models here.


# @admin.register(Blog)
# class BlogAdmin(admin.ModelAdmin):
#     readonly_fields = ["blog_photo", "created_at", "updated_at"]
#     prepopulated_fields = {"slug": ["title"]}
#     filter_horizontal = ["tags"]

#     list_display = [
#         "id",
#         "title",
#         "slug",
#         "blog_photo",
#         "author",
#         "created_at",
#         "is_published",
#         "content_info",
#     ]
#     list_filter = ["author", "is_published"]
#     search_fields = ["title", "content", "author__name"]
#     list_display_links = ["id", "title"]

#     ordering = ["created_at", "title"]
#     list_editable = ["is_published", "author"]
#     list_per_page = 5
#     actions = ["publish"]

#     save_on_top = True

#     @admin.display(description="Длина Контента")
#     def content_info(self, blog: Blog):
#         return f"Длина Контента {len(blog.content)}"

#     @admin.display(description="Фото")
#     def blog_photo(self, blog: Blog):
#         if blog.image:
#             return mark_safe(
#                 f"<a href='{blog.image.url}' target='_blank'><img src ='{blog.image.url}' width = 100></a>"
#             )

#     @admin.action(description="Опубликовать выбранные записи")
#     def publish(self, request, queryset):
#         count = queryset.update(is_published=True)
#         self.message_user(request, f"Опубликовано {count} записей", messages.SUCCESS)


# @admin.register(Author)
# class AuthorAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ["author_name"]}
#     list_display = ["id", "author_name", "slug", "email", "phone"]
#     search_fields = ["author_name", "email", "phone"]
#     list_display_links = ["id", "author_name"]

#     list_editable = ["email", "phone"]
#     list_per_page = 5


# @admin.register(Tags)
# class TagsAdmin(admin.ModelAdmin):
#     list_display = ["id", "tag_name", "slug"]
#     search_fields = ["tag_name"]
#     list_display_links = ["id", "tag_name"]
#     prepopulated_fields = {"slug": ["tag_name"]}


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ["id", "category_name", "slug"]
#     search_fields = ["category_name"]
#     list_display_links = ["id", "category_name"]
#     prepopulated_fields = {"slug": ["category_name"]}