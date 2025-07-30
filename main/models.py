from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} with this email: '{self.email}' said {self.message[:20]}"
    
    
class PortfolioItem(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    image = models.ImageField(upload_to='portfolio_images/', verbose_name='عکس نمونه‌کار')
    project_url = models.URLField(blank=True, null=True, verbose_name='لینک پروژه')
    image = models.ImageField(upload_to='portfolio_images/', verbose_name='عکس نمونه‌کار')
    slug = models.SlugField(unique=True, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('portfolio_detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
    
    
class Service(models.Model):
    title = models.CharField(max_length=100, verbose_name='title')
    description = models.TextField(verbose_name='description')
    icon = models.CharField(max_length=50, verbose_name='bootstrap icon', help_text='like: bi-code-slash')
    order = models.PositiveIntegerField(default=0, verbose_name='order by')

    class Meta:
        ordering = ['order']
        verbose_name = 'service/skill'
        verbose_name_plural = 'services/skills'

    def __str__(self):
        return self.title
