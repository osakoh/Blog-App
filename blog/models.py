from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

"""
Django QuerySets are lazy, which means they are only evaluated when they are forced to be. 
This behavior makes QuerySets very efficient. You can use the filter() method of the manager to filter a QuerySet.
Certain results can be exclude from your QuerySet using the exclude() method of the manager.
A canonical URL is the preferred URL for a resource. The Django convention is to add a get_absolute_url() method to the 
model that returns the canonical URL for the object. The reverse() method allows you to build URLs by their name and pass optional parameters
"""


# custom manager, 'PublishedManager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


# allows user to create and post a blog
class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    # when the user is deleted, the database will also delete all related blog posts. if no 'related_name' is defined,
    # django uses the model name in lowercase, followed by '_set'  to name the relationship of the related object
    # to the object of the model, i.e 'post_set'
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=200, unique=True)  # unique=True: to ensure that a title should not be repeated
    slug = models.SlugField(max_length=200, unique_for_date='publish')  # publish date is used to build the slug
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)  # returns the current datetime in a timezone

    # date will be saved automatically when a blog is created in the database
    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)  # changes whenever the 'save' button is pressed
    # shows the status of a post. The 'choices' parameter sets the value of the field
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    # objects = models.Manager()  # default manager
    published = PublishedManager()  # custom manager

    class Meta:
        ordering = ('-publish',)  # sort according to the latest/newest post

    # returns a string representation
    def __str__(self):
        return self.title

    # used to link to a specific post i.e blog_post_detail
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


# comments section
# The save() method is available for ModelForm but not for Form instances, since they are not linked to any model.
class Comment(models.Model):
    # This many-to-one relationship as  each post may have multiple comments. if no 'related_name' is defined, django
    # uses the model name in lowercase, followed by '_set'  to name the relationship of the related object to the
    # object of the model, i.e 'comment_set'
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=25)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)  # date added to db the first time it's created
    updated = models.DateTimeField(auto_now=True)  # date added whenever the 'save' button is pressed
    active = models.BooleanField(default=True)  # to manually deactivate inappropriate comments

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

