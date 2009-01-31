# -*- coding: utf-8 -*-
from copy import deepcopy, copy

from django.db import models
from django.db import connection

from turbion.core.utils.models import GenericManager
from turbion.core.tags.managers import BaseTaggedModelManager
from turbion.core.comments.models import Comment
from turbion.core.tags.models import TaggedItem
from turbion.core.utils.descriptor import to_descriptor

class BlogManager(models.Manager):
    def get_oldest(self):
        try:
            return self.all().order_by("created_on")[0]#FIXME: select_related
        except IndexError:
            raise self.model.DoesNotExist

    def create_blog(self, name, slug, owner):

        blog = self.create(name=name, slug=slug, created_by=owner)

        owner.grant_capabilities(set="blog.caps", instance=blog)

        return blog

class PostManager(GenericManager, BaseTaggedModelManager):
    def get_query_set(self):
        return super(PostManager, self).get_query_set().select_related("created_by", "blog")

    def for_blog(self, blog):
        return self.filter(blog=blog)

    def for_user(self, blog, user):
        return self.filter(
                        blog=blog,
                        author=user
                )

    def for_tag(self, blog, tag):
        return super(PostManager, self).for_tag(tag, self.for_blog(blog))
