# -*- coding: utf-8 -*-
from copy import deepcopy, copy

from django.db import models
from django.db import connection

from turbion.core.utils.models import GenericManager
from turbion.core.tags.managers import BaseTaggedModelManager
from turbion.core.comments.models import Comment
from turbion.core.tags.models import TaggedItem
from turbion.core.utils.descriptor import to_descriptor


def create_blog(self, owner):
    owner.grant_capability(set="blog.caps")

class PostManager(GenericManager, BaseTaggedModelManager):
    def get_query_set(self):
        return super(PostManager, self).get_query_set().select_related("created_by")

    def for_tag(self, tag):
        return super(PostManager, self).for_tag(tag, self.all())
