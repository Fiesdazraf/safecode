from django.db import models
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='نام دسته‌بندی')

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="title")
    content = models.TextField(verbose_name="content")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="category")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="start date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="update date")
    slug = models.SlugField(unique=True, blank=True, verbose_name="slug") 
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
        
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100, verbose_name='نام')
    content = models.TextField(verbose_name='متن نظر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    def __str__(self):
        return f"نظر توسط {self.name} روی «{self.post}»"
