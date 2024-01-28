from django.contrib import sitemaps
from django.urls import reverse

class AssignmentSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ['assignment:submit_topic', 'assignment:generate_assignment', 'assignment:generate_essay']
   
    def location(self, item):
        return reverse(item)
