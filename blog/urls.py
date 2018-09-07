from django.urls import path
from . import views

# import to instantiate feed
from .feeds import LatestPostsFeed


app_name = 'blog'

urlpatterns = [
    #
    path('feed/', LatestPostsFeed(), name='post_feed'),

    # post views
    # calls the post_list view without any optional parameters
    path('', views.post_list, name='post_list'),

    # calls the view with the tag_slug parameter.
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),

    # path('', views.PostListView.as_view(), name='post_list'),

    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail,
         name='post_detail'),

    path('<int:post_id>/share/', views.post_share, name='post_share'),

    path('search/', views.post_search, name='post_search'),
]
