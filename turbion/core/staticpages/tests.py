# -*- coding: utf-8 -*-
from turbion.core.blogs.utils import reverse
from turbion.core.utils.testing import BaseViewTest
from turbion.core.staticpages.models import Page
from turbion.core.blogs.models import Blog
from turbion.core.profiles.models import Profile

class StaticPagesViews(BaseViewTest):
    fixtures = ["turbion/test/profiles", "turbion/test/blogs"]

    def setUp(self):
        blog = Blog.objects.all()[0]
        profile = Profile.objects.all()[0]

        self.page = Page.objects.create(
            blog=blog,
            created_by=profile,
            title="Test page",
            slug="testpage",
            text="Some text"
        )
        self.blog = blog

        for i in range(5):
            Page.objects.create(
                blog=blog,
                created_by=profile,
                title="Test page with num %s" % i,
                slug="testpage%s" % i,
                text="Some text"
            )

    def test_page(self):
        response = self.assertStatus(self.page.get_absolute_url())

    def test_sitemap(self):
        response = self.assertStatus(reverse("turbion_pages_sitemap", args=[self.blog.slug,]))
