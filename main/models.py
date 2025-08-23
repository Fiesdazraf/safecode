from django import forms
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from django.db import models

class Contact(models.Model):
    name = models.CharField("name", max_length=100)
    email = models.EmailField("email")
    message = models.TextField("message")
    created_at = models.DateTimeField("created at", auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # پیش‌فرض آخرین پیام‌ها اول
        verbose_name = "Contacts message"
        verbose_name_plural = "Contacts messages"

    def __str__(self):
        snippet = (self.message[:20] + "…") if len(self.message) > 20 else self.message
        return f"{self.name} ({self.email}) → {snippet}"

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ("name", "email", "message")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        base = (
            "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm "
            "focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 "
            "placeholder:text-slate-400 bg-white"
        )
        self.fields["name"].widget.attrs.update({
            "class": base, "dir": "rtl", "placeholder": "نام شما"
        })
        self.fields["email"].widget.attrs.update({
            "class": base, "dir": "rtl", "placeholder": "ایمیل شما"
        })
        self.fields["message"].widget.attrs.update({
            "class": base, "dir": "rtl", "rows": 6, "placeholder": "متن پیام…"
        })
    
class PortfolioItem(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.CharField(max_length=250, verbose_name="Short description")
    icon_path = models.CharField(
        max_length=200, blank=True, null=True,
        verbose_name="Icon path (static/icons)",
        help_text="Only the file name, e.g. cms.svg"
    )
    image = models.ImageField(
        upload_to="portfolio_images/", blank=True, null=True,
        verbose_name="Cover image"
    )
    project_url = models.CharField(
        max_length=200, blank=True, null=True,
        verbose_name="Demo/Project link"
    )
    repo_url = models.URLField(
        blank=True, null=True, verbose_name="Source code link"
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    sort_order = models.PositiveIntegerField(
        default=0, verbose_name="Sort order",
        help_text="Higher numbers will appear first"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        ordering = ["-sort_order", "-created_at"]  # sort by order first, then date

    def __str__(self):
        return self.title
    
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

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ("title", "description", "icon", "order")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base = "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm " \
               "focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 " \
               "placeholder:text-slate-400 bg-white"
        self.fields["title"].widget.attrs.update({"class": base, "placeholder": "عنوان خدمت"})
        self.fields["description"].widget.attrs.update({"class": base, "rows": 4, "placeholder": "توضیحات"})
        self.fields["icon"].widget.attrs.update({"class": base, "placeholder": "مثلاً: bi-code-slash"})
        self.fields["order"].widget.attrs.update({"class": base, "placeholder": "ترتیب نمایش"})
