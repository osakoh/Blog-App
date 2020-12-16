from django.urls import path
from . import views

app_name = 'blog'  # allows URLs to be organised by application.

urlpatterns = [
    # path('', views.blog_post_list, name='post_list'),
    path('', views.BlogPostList.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.blog_post_detail, name='post_detail'),
    path('<int:post_id>/share', views.post_share, name='post_share'),
]