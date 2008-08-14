# -*- coding: utf-8 -*-
from copy import deepcopy, copy

from django.db import models
from django.db import connection
from django.contrib.contenttypes.models import ContentType

from turbion.utils.models import GenericManager

from turbion.comments.models import Comment
from turbion.tags.models import TaggedItem

quote_name             = connection.ops.quote_name
taggeditems_table_name = quote_name(TaggedItem._meta.db_table)

class BlogManager(models.Manager):
    def get_oldest(self):
        try:
            return self.all().order_by("created_on")[0]#FIXME: select_related
        except IndexError:
            raise self.model.DoesNotExist

class PostManager(GenericManager):
    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self.model)

    @property
    def table_name(self):
        return quote_name( self.model._meta.db_table)

    def get_query_set(self):
        return super(PostManager, self).get_query_set().select_related("created_by", "blog")

    def for_blog(self, blog):
        return self.filter(blog=blog)

    def for_user(self, blog, user):
        return self.filter(blog=blog,
                           author=user)

    def for_tag(self, blog, tag):
        return self.filter(blog=blog).extra(where=["%s.tag_id = %s" % (taggeditems_table_name, tag.id),
                                                           "%s.item_ct_id = %s" % (taggeditems_table_name, self.content_type.id),
                                                           "%s.item_id = %s.id" % (taggeditems_table_name, self.table_name)],
                                            tables=[TaggedItem._meta.db_table])
