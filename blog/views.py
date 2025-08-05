import random
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages


# Create your views here.

def post_list(request):
    post_list = Post.objects.order_by('-created_at')
    paginator = Paginator(post_list, 6)  # هر صفحه ۶ پست

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # آمار سریع
    total_posts = Post.objects.count()
    try:
        from .models import Category  # اگه Category داری
        categories_count = Category.objects.count()
    except ImportError:
        categories_count = None

    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
        'total_posts': total_posts,
        'categories_count': categories_count,
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    all_posts = list(Post.objects.exclude(slug=slug))
    random_posts = random.sample(all_posts, min(3, len(all_posts)))

    comments = post.comments.order_by('-created_at')
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', slug=post.slug)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'random_posts': random_posts,
        'comments': comments,
        'form': form
    })
    
    

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form': form})



def dashboard(request):
    posts = Post.objects.order_by('-created_at')
    total_comments = Comment.objects.count()
    return render(request, 'blog/dashboard.html', {'posts': posts, 'total_comments': total_comments})



def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "پست با موفقیت ویرایش شد.")
            return redirect('blog:dashboard')
    else:
        form = PostForm(instance=post)
        

    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})



def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        post.delete()
        messages.success(request, "پست با موفقیت حذف شد.")
        return redirect('blog:dashboard')

    return render(request, 'blog/post_delete_confirm.html', {'post': post})



def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_slug = comment.post.slug
    comment.delete()
    return redirect('blog:dashboard')  # یا به post_detail برگردی اگه خواستی
