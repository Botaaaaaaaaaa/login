# Generated by Django 5.0.1 on 2024-02-01 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_remove_blog_updamed_at_blog_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='new',
        ),
    ]
