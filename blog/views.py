from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
# from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm

from django.core.mail import send_mail

from taggit.models import Tag

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# This function will allow us to perform aggregated counts of tags.
from django.db.models import Count

# search vector for postgres
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity


# Create your views here.

# It takes an optional tag_slug parameter that has a None default
# value. This parameter will come in the URL.
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag})


# class PostListView(ListView):
#     queryset = Post.published.all()
#     # The default variable name is "object_list" if no context_object_name
#     # is specified
#     context_object_name = 'posts'
#     # Paginate the result displaying three objects per page.
#     paginate_by = 3
#     # If we don't set a default template, ListView will use blog/post_list.html.
#     template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # retrieves the list of active comments for this post, using the manager for
    # related objects defined in "comments" using the related_name attribute
    comments = post.comments.filter(active=True)

    # for adding a new comment
    new_comment = None
    #
    if request.method == 'POST':
        #  to let users add a new comment using a form instance with
        # (comment_form = CommentForm() if the view is called by a 'GET' request,
        # if the view is called by 'POST', the form is instantiated using the
        # submitted data and validate it using 'is_valid()' method)
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # creates the object, but don't save to DB,
            # using commit=False creates the model instance.
            # the new comment created is assigned to the new_comment variable
            new_comment = comment_form.save(commit=False)

            # assigns the current post to the comment created
            # meaning the new comment belongs to the given post
            new_comment.post = post

            # saves the comment to the DB
            new_comment.save()
    else:
        comment_form = CommentForm()

    #  List similar post

    # retrieves a Python list of IDs for the tags of the current post.
    # The values_list() QuerySet returns tuples with the values for the given
    # fields. We pass flat=True to it to get a flat list like [1, 2, 3, ...].
    post_tags_ids = post.tags.values_list('id', flat=True)

    # gets all the posts that contain any of these tags, excluding the current post itself.
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)

    # - the Count aggregation function to generates a
    # calculated field—same_tags—that contains the number of tags
    # shared with all the tags queried.
    # - order the result by the number of shared tags(descending order) and by
    # publish to display recent posts first for the posts with the same
    # number of shared tags.
    # -We slice the result to retrieve only the first four posts.
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts})


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

     # checks if the email form was submitted(POST method)
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


# the search view
# def post_search(request):
#     form = SearchForm()
#     query = None
#     results = []
#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             results = Post.objects.annotate(
#                 similarity=TrigramSimilarity('title', query),
#             ).filter(similarity__gt=0.3).order_by('-similarity')
#     return render(request,
#                   'blog/post/search.html',
#                   {'form': form,
#                    'query': query,
#                    'results': results})


def post_search(request):
    # instantiate the search form
    form = SearchForm
    query = None
    results = []
    # to check if the form is submitted, we look for the query parameter in the request.GET dictionary
    if 'query' in request.GET:
        # submitting the form using the GET method makes the URL include the query parameter
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            # results = Post.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
            results = Post.objects.annotate(search=search_vector,
                                            rank=SearchRank(search_vector, search_query)).\
                filter(search=search_query).order_by('-rank')

    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'result': results})



# Remember that QuerySets are lazy. The QuerySets to retrieve posts
# will only be evaluated when we loop over the post list when
# rendering the template.
