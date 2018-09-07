"""
A web feed is a data format (usually XML) that provides users
with frequently updated content. Users will be able to subscribe
to your feed using a feed aggregator, a software that is used
to read feeds and get new content notifications.
"""

from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

# title, link and description correspond to the standard RSS
#  <title>, <link> and <description> elements, respectively.


class LatestPostsFeed(Feed):
    title = 'My blog'
    link = '/blog/'
    description = 'New posts of my blog.'

    # - The items() method retrieves the objects to be included in the feed.
    # only the last five published post is retrieved
    def items(self):
        return Post.published.all()[:5]

    # - item_title() method receives each object returned by items()
    # and return the title for each item
    def item_title(self, item):
        return item.title

    # - item_description() method receives each object returned by items()
    # and return description for each item.
    def item_description(self, item):
        # the truncatewords built-in template filter to build the
        #  description of the blog post with the first 30 words.
        return truncatewords(item.body, 30)

# then we instantiate the feed in the url.py
