from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.core.mail import send_mail

from .models import Post, Comment
from .forms import CommentForm, EmailPostForm
from my_settings import Configure

"""
# displays all the published blogs using the 'published manager'
def blog_post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # instantiate the Paginator class and specifies only 3 posts per page
    page = request.GET.get('page')  # page GET parameter indicates the current page number
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)  # if the page parameter is not an integer, return the first page
    except EmptyPage:
        # if page parameter is a number higher than the last page (out of range), show the last page
        posts = paginator.page(paginator.num_pages)
    return render(request, 'post/list.html', {'posts': posts, 'page': page})  # pass the page number and  objects to the template.
"""


# 'page_obj' is the variable for django's generic 'ListView'
class BlogPostList(ListView):
    queryset = Post.published.all()
    # queryset = Post.objects.all()
    context_object_name = 'posts'  # default variable is 'object_list' if no name is specified
    paginate_by = 3  # three objects per page.
    template_name = 'post/list.html'  # django uses 'blog/post_list.html' as default if template name isn't given


# recall the *unique_for_date='publish'* parameter was used to build the slug field. Meaning,
# there will only be one post with a slug for a given year, month, and day.
# Template tags {% tag %}: controls how the template is rendered.
# Template variables {{ variable }}: get replaced with values when the template is rendered.
# Template filters {{ variable|filter }}: allow you to modify variables for display.
def blog_post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=post
                             )
    # using the 'related_name', 'comments', each comment is linked to a post and then filtered using 'active=True'
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':  # user clicks send
        comment_form = CommentForm(request.POST)  # create a form instance with the submitted data
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)  # creates a comment obj using 'save()', but don't save to db
            new_comment.post = post  # assigns current post to the comment
            print(new_comment.post)
            new_comment.save()  # saves the comment to the db
    else:
        comment_form = CommentForm()  # creates a new form instance to display the empty form
    context = {'post': post,
               'comments': comments,
               'new_comment': new_comment,
               'comment_form': comment_form}
    return render(request, 'post/detail.html', context)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')  # get post by id
    sent = False
    c = Configure()

    if request.method == "POST" or None:  # when the user fills the form and submits it
        form = EmailPostForm(request.POST or None)  # create a form instance with the submitted data
        if form.is_valid():  # If the form is valid
            cd = form.cleaned_data  # by form.cleaned_data: retrieves the validated data

            # request.build_absolute_uri(): to build a complete URL, including the HTTP schema and hostname
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n {cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, c.usr, [cd['to']])

            sent = True  # when the mail sends successfully
            return redirect('blog:post_list')
        # else:
        #     print(form.errors)

    else:
        # when the page is loaded initially, it is a GET request, then the form instance is displayed
        # show an empty form if method is GET(i.e user doesn't fill the form)
        form = EmailPostForm()

    content = {'post': post, 'form': form, 'sent': sent}
    return render(request, 'post/share.html', content)
