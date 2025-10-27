from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from properties.models import Property
from blog.models import BlogPost
from agents.models import Agent

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return ['home', 'properties:property_list', 'about', 'contact', 'agents:agent_list']

    def location(self, item):
        return reverse(item)

class PropertySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Property.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

class AgentSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Agent.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at