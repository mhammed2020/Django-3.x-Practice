from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, get_object_or_404
from .models import Post
    

# pagination 

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def post_list(request):
    # posts = Post.published.all()
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) 
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,
    'blog/post/list.html',
    {    'page': page,
        'posts': posts
    })



def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
status='published',
publish__year=year,
publish__month=month,
publish__day=day)

    return render(request,
    'blog/post/detail.html',
    {'post': post})


# Using class-based views .. an other logic .. fast

from django.views.generic import ListView
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'



# Handling forms in views

from .forms import EmailPostForm
"""
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')

    if request.method == 'POST':
    # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
# Form fields passed validation
            cd = form.cleaned_data
# ... send email
        else:
            form = EmailPostForm()
        return render(request, 'blog/post/share.html', {'post': post,
'form': form})


 """
# sen

from django.core.mail import send_mail
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
            post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
            f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'jeddou.mhammed@gmail.com',
            [cd['jeddou.mhammed@gmail.com']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
    'form': form,
    'sent': sent})