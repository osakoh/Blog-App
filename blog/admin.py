from django.contrib import admin
from .models import Post, Comment

# Register your models here.


# @admin.register() decorator performs the same function as the admin.site.register() function we
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # list_display: set the fields of your model that you want to display
    # in the admin object list page. The list page now includes a right
    # sidebar that allows you to filter the results by the fields included
    # in the list_filter attribute.
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    # creates a search bar
    search_fields = ('title', 'body')
    # the slug field gets prepopulated based on the input in the title
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')



# admin.site.register(Post)
