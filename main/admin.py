from django.contrib import admin
from .models import Contact, PortfolioItem, Service

admin.site.register(Contact)
admin.site.register(PortfolioItem)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    ordering = ('order',)
