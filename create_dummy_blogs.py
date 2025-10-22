import os
import django
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dreamhomes.settings')
django.setup()

# ✅ Import your correct models
from accounts.models import CustomUser
from blog.models import BlogCategory, BlogTag, BlogPost


def create_blog_data():
    # ✅ Create or get author (CustomUser)
    author, created = CustomUser.objects.get_or_create(
        username='rajesh_agent',
        defaults={
            'first_name': 'Rajesh',
            'last_name': 'Sharma',
            'email': 'rajesh.sharma@dreamhomes.com',
            'password': 'testpass123'
        }
    )

    # ✅ Create categories
    categories_data = [
        {'name': 'Buying Guide', 'slug': 'buying-guide'},
        {'name': 'Selling Tips', 'slug': 'selling-tips'},
        {'name': 'Market Trends', 'slug': 'market-trends'},
        {'name': 'Home Improvement', 'slug': 'home-improvement'},
        {'name': 'Investment', 'slug': 'investment'},
        {'name': 'First Time Buyers', 'slug': 'first-time-buyers'},
    ]

    categories = {}
    for cat_data in categories_data:
        category, _ = BlogCategory.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        categories[cat_data['slug']] = category

    # ✅ Create tags
    tags_data = [
        {'name': 'Real Estate', 'slug': 'real-estate'},
        {'name': 'Nagpur', 'slug': 'nagpur'},
        {'name': 'Property', 'slug': 'property'},
        {'name': 'Home', 'slug': 'home'},
        {'name': 'Investment', 'slug': 'investment-tag'},
        {'name': 'Market', 'slug': 'market'},
    ]

    tags = {}
    for tag_data in tags_data:
        tag, _ = BlogTag.objects.get_or_create(
            slug=tag_data['slug'],
            defaults=tag_data
        )
        tags[tag_data['slug']] = tag

    # ✅ Create blog posts
    posts_data = [
        {
            'title': '10 Essential Tips for First-Time Home Buyers in Nagpur',
            'slug': 'first-time-home-buyers-tips',
            'summary': 'Discover the key steps and considerations for first-time home buyers in the Nagpur real estate market.',
            'content': '''
                <h2>Understanding the Nagpur Real Estate Market</h2>
                <p>Nagpur's real estate market has been growing steadily, offering great opportunities for first-time buyers...</p>
            ''',
            'categories': ['first-time-buyers', 'buying-guide'],
            'tags': ['real-estate', 'nagpur', 'home'],
            'featured': True,
            'read_time': 8,
        },
        {
            'title': 'Nagpur Property Market Trends 2024',
            'slug': 'nagpur-property-market-trends-2024',
            'summary': 'Analysis of current real estate trends in Nagpur and predictions for the coming year.',
            'content': '''
                <h2>Current Market Overview</h2>
                <p>The Nagpur real estate market has shown remarkable resilience in 2024...</p>
            ''',
            'categories': ['market-trends'],
            'tags': ['market', 'nagpur', 'investment-tag'],
            'featured': True,
            'read_time': 6,
        },
    ]

    for post_data in posts_data:
        post, created = BlogPost.objects.get_or_create(
            slug=post_data['slug'],
            defaults={
                'title': post_data['title'],
                'author': author,
                'summary': post_data['summary'],
                'content': post_data['content'],
                'status': 'published',
                'featured': post_data.get('featured', False),
                'read_time': post_data.get('read_time', 5),
                'published_date': timezone.now() - timedelta(days=len(posts_data) - posts_data.index(post_data))
            }
        )

        if created:
            # Add categories
            for cat_slug in post_data['categories']:
                post.categories.add(categories[cat_slug])

            # Add tags
            for tag_slug in post_data['tags']:
                post.tags.add(tags[tag_slug])

            print(f"✅ Created post: {post.title}")

    print("🎉 Blog dummy data created successfully!")


if __name__ == '__main__':
    create_blog_data()
