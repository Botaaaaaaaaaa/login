from django import template

from ..models import Category,Tags

register = template.Library()

@register.simple_tag
def blog_tag():
    return "Blog"

@register.inclusion_tag("blog/blog_card.html")
def template_blog(posts):
    return{"posts": posts}

@register.inclusion_tag("blog/categories_card.html")
def categories_block():
    categories = Category.objects.all()
    return{"categories": categories}

@register.inclusion_tag("blog/tag_card.html")
def tags_block():
    tags= Tags.objects.all()
    return {"tags" : tags}

@register.inclusion_tag("blog/pagination_card.html")
def pagination_block(page,pagination,paginator):
    return {"page": page, "pagination": pagination, "paginator": paginator}