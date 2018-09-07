# The way you name the file is important. You will use the name
# of this module to load tags in templates.

from django import template
from ..models import Post
from django.db.models import Count

from django.utils.safestring import mark_safe
import markdown

# - Each template tags module must contain a variable
# called (register) to be a valid tag library.
# - This variable(register) is an instance of template.Library,
#  and it's used to register your own template tags and filters.
register = template.Library()


# - the @register.simple_tag decorator registers the function as a simple tag.
# - Django uses the function's name(total_post) as the
# tag name.
# - To register it using a different name, do it by
# specifying a name attribute,
# such as @register.simple_tag(name='my_tag').
# - restart the Django development server in order to use
# the new tags and filters in templates.
# - before the custom template tags can be used, you have to
# make them available for the template using the {% load %}tag.
# - Use the name of the Python module containing
# your template tags and filters.
@register.simple_tag
def total_post():
    return Post.published.count()


# Displays the latest post in the sidebar using inclusion tag(returns a template)
@register.inclusion_tag('blog/post/latest_posts.html')
# - The count parameter defaults to 5. This parameter allows us to specify the
# number of posts we want# to display.
# - The optional argument count. Is a variable(count) used to limit the results
# of the query Post.published.order_by('-publish')[:count].
# - This template tag created allows you to specify the optional
# number of posts to display as {% show_latest_posts 3 %}.
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# Assignment tag to display the most commented post
@register.simple_tag
def get_most_commented_posts(count=3):
    # - A QuerySet using the annotate() function to aggregate the total number
    # of comments for each post.
    # - The Count aggregation function stores the number of comments in the
    # computed field(in a descending order) total_comments for each Post object.
    #  - The optional count variable to limit the total number of objects returned.
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
# - To avoid a collision between our function name and the markdown module,
# the function name is called markdown_format.
def markdown_format(text):
    # - - To avoid a collision between our function name and the markdown module,
    # the filter markdown name for usage in templates, such as {{ variable|markdown }}.
    return mark_safe(markdown.markdown(text))
# The mark_safe function provided by Django marks the result as safe HTML to be
# rendered in the template.
