from django.contrib import admin
from .models import BlogCategory, BlogTag, BlogPost, BlogNewsletterSubscriber, BlogComment

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date', 'status', 'featured']
    list_filter = ['status', 'categories', 'published_date', 'featured']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    filter_horizontal = ['categories', 'tags']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')

@admin.register(BlogNewsletterSubscriber)
class BlogNewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_date', 'is_active']
    list_filter = ['is_active', 'subscribed_date']
    search_fields = ['email']

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created_date', 'approved']
    list_filter = ['approved', 'created_date']
    search_fields = ['name', 'email', 'content']
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = "Approve selected comments"