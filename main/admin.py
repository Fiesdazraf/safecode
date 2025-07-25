from django.contrib import admin
from .models import Contact, PortfolioItem

# Register your models here.
admin.site.register(Contact)

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
