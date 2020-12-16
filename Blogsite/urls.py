from django.contrib import admin
from django.urls import path, include


"""
You include these patterns under the namespace blog. Namespaces have to be unique across your entire project. 
The blog URLs can easily be accessed by using the namespace followed by a colon and the URL name, 
e.g, blog:post_list and blog:post_detail. 
"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
]
