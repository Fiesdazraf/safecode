from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import PortfolioItem

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return ['home', 'portfolio', 'contact']

    def location(self, item):
        return reverse(item)
    
class PortfolioSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return PortfolioItem.objects.all()

