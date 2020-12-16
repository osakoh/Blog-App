from django.contrib import admin
from .models import Post, Comment


# adds the blog model to the admin
@admin.register(Post)  # same as 'admin.site.register(Post)'
# customises the admin view
class PostAdmin(admin.ModelAdmin):
    # 'list_display' sets fields to be displayed on the admin page
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_editable = ('status',)
    list_filter = ('status', 'created', 'publish', 'author')  # shows a filter section on the admin site
    search_fields = ('title', 'body')  # creates a search bar that searches the title and body field
    prepopulated_fields = {'slug': ('title',)}  # automatically pre-populates the slug field from the title
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'  # creates a sort of date (yr & month) breadcrumbs
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_editable = ('active',)
    list_filter = ('active', 'created', 'updated')   # shows a filter section on the comment admin site
    search_fields = ('name', 'email', 'body')   # creates a search field that searches the name, email and body field