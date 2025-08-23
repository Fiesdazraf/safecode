from django.contrib import admin
from .models import Contact, PortfolioItem, Service

# Contact registered simply
admin.site.register(Contact)

# Service admin
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "icon")
    list_editable = ("order",)
    search_fields = ("title", "description")
    ordering = ("order",)

# Portfolio admin
@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ("title", "sort_order", "project_url", "created_at")
    list_editable = ("sort_order",)  # allow inline editing
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-sort_order", "-created_at")
