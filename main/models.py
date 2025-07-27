from django.db import models

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

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return self.title

