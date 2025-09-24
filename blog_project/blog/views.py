from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Category, Comment
from .forms import CommentForm

def get_common_context():
    """Helper function to get common context data"""
    return {
        'categories': Category.objects.all(),
        'recent_posts': Post.objects.filter(status='published')[:5],
    }

def post_list(request):
    posts = Post.objects.filter(status='published')
    
    # Pagination
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        **get_common_context(),
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        publish_date__year=year,
        publish_date__month=month,
        publish_date__day=day,
        slug=slug,
        status='published'
    )
    
    comments = post.comments.filter(active=True)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        **get_common_context(),
    }
    return render(request, 'blog/post_detail.html', context)

def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category, status='published')
    
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        **get_common_context(),
    }
    return render(request, 'blog/category_posts.html', context)