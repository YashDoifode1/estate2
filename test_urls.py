# test_urls.py
from django.test import TestCase
from django.urls import reverse, resolve

class BlogURLTests(TestCase):
    def test_blog_list_url(self):
        url = reverse('blog_list')
        self.assertEqual(url, '/blog/')
    
    def test_blog_detail_url(self):
        url = reverse('blog_detail', kwargs={'slug': 'test-post'})
        self.assertEqual(url, '/blog/test-post/')