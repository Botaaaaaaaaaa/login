from django.db import models


# Create your models here.
class LinkPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=100)
    # created_at = models.DateTimeField(auto_now_add=True)

    # updated_at = models.DateTimeField(auto_now=True)
    # is_published = models.BooleanField(default=True)

    # class Meta:
    #     db_table = ""