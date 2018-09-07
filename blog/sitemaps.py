"""
A sitemap is an XML file that tells search engines the pages of your website,
their relevance, and how frequently they are updated. Using a sitemap,
you will help crawlers that index your website's content.
"""

from django.contrib.sitemaps import Sitemap
from .models import Post

# The changefreq and priority attributes indicate the change frequency of the
# post pages and their relevance in the website (the maximum value is 1).


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    # - The items() method returns the QuerySet of objects to include in this
    # sitemap.
    # - By default, Django calls the get_absolute_url() method on each
    # object to retrieve its URL created earlier.
    # - To specify the URL for each object, you can add a location method to
    # your sitemap class.
    def items(self):
        return Post.published.all()

    # The lastmod method receives each object returned
    # by items() and returns the last time the object was modified.
    def lastmod(self, obj):
        return obj.updated


# Both changefreq and priority methods can also be either methods or attributes.
