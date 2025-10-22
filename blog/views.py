from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from django.http import JsonResponse
from .models import BlogPost, BlogCategory, BlogNewsletterSubscriber
from .forms import BlogNewsletterForm, BlogCommentForm

def blog_list(request):
    # Get all published posts
    posts = BlogPost.objects.filter(status='published')
    
    # Handle category filter
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(categories__slug=category_slug)
    
    # Handle search
    search_query = request.GET.get('q')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(summary__icontains=search_query) |
            Q(categories__name__icontains=search_query)
        ).distinct()
    
    # Pagination
    paginator = Paginator(posts, 9)  # 9 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories with post counts
    categories = BlogCategory.objects.annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    ).filter(post_count__gt=0)
    
    # Get popular posts (most viewed)
    popular_posts = BlogPost.objects.filter(status='published').order_by('-views')[:5]
    
    # Newsletter form
    newsletter_form = BlogNewsletterForm()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'popular_posts': popular_posts,
        'newsletter_form': newsletter_form,
    }
    
    return render(request, 'blog/blog.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    
    # Increment view count
    post.views += 1
    post.save()
    
    # Get related posts (same categories)
    related_posts = BlogPost.objects.filter(
        categories__in=post.categories.all(),
        status='published'
    ).exclude(id=post.id).distinct()[:3]
    
    # Get recent posts
    recent_posts = BlogPost.objects.filter(status='published').exclude(id=post.id)[:5]
    
    # Get categories with post counts
    categories = BlogCategory.objects.annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    ).filter(post_count__gt=0)
    
    # Comment form
    comment_form = BlogCommentForm()
    
    # Newsletter form
    newsletter_form = BlogNewsletterForm()
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'recent_posts': recent_posts,
        'categories': categories,
        'comment_form': comment_form,
        'newsletter_form': newsletter_form,
    }
    
    return render(request, 'blog/blog-detail.html', context)

def newsletter_subscribe(request):
    if request.method == 'POST':
        form = BlogNewsletterForm(request.POST)
        if form.is_valid():
            subscriber, created = BlogNewsletterSubscriber.objects.get_or_create(
                email=form.cleaned_data['email'],
                defaults={'is_active': True}
            )
            
            if not created:
                subscriber.is_active = True
                subscriber.save()
                messages.success(request, 'You have been resubscribed to our newsletter!')
            else:
                messages.success(request, 'Thank you for subscribing to our newsletter!')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False, 
                    'error': form.errors['email'][0]
                })
    
    return redirect('blog_list')

def add_comment(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    
    if request.method == 'POST':
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Your comment has been submitted and is awaiting approval.')
    
    return redirect('blog_detail', slug=slug)