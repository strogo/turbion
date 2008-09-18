# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from turbion.utils.testing import BaseViewTest
from turbion.staticpages.models import Page
from turbion.blogs.models import Blog
from turbion.profiles.models import Profile

class StaticPagesViews(BaseViewTest):
    fixtures = ["profiles", "blog"]
    
    def setUp(self):
        blog = Blog.objects.all()[0]
        profile = Profile.objects.all()[0]
        
        self.page = Page.objects.create(
            blog=blog,
            created_by=profile,
            title="Test page",
            text="Some text"            
        )
        self.blog = blog
        
        for i in range(5):
            Page.objects.create(
                blog=blog,
                created_by=profile,
                title="Test page with num %s" % i,
                text="Some text"
            )
    
    def test_page(self):
        response = self.assertStatus(reverse("pages_dispatcher", args=[self.blog.slug, self.page.slug]))
        print response
    
    def test_sitemap(self):
        self.assertStatus(reverse("pages_sitemap", args=[self.blog.slug,]))