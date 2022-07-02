from django.db import models
from django.urls import reverse
from apps.user.models import User, NewsReader

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=200)
    category_slug = models.SlugField(max_length=200, unique=True)

    def __int__(self):
        return self.category_slug

    def __str__(self):
        return 'Category: ' + self.category_name 

class News(models.Model):
    news_slug = models.SlugField(max_length=200, unique=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True)
    description = models.TextField(null=True)
    reported_by = models.CharField(max_length=200)
    reported_at = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __int__(self):
        return self.news_slug

    def __str__(self):
        return 'News: ' + self.title

