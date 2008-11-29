# -*- coding: utf-8 -*-
from django.db import models, connection

from turbion.utils.descriptor import to_descriptor

quote_name = connection.ops.quote_name

class TagManager(models.Manager):
    def filter_for_object(self, obj):
        from turbion.tags.models import TaggedItem, Tag
        pks = TaggedItem.objects.filter_for_object(obj).values_list("tag", flat=True).distinct()

        return Tag.objects.filter(pk__in=pks.query)

    def filter_for_model(self, model, **kwargs):
        from turbion.tags.models import TaggedItem, Tag
        pks = TaggedItem.objects.filter_for_model(model, **kwargs).values_list("tag", flat=True).distinct()

        return Tag.objects.filter(pk__in=pks.query)

    def create_tag(self, tag):
        if isinstance(tag, (long, int)):
            tag = self.get(pk=tag)
        elif isinstance(tag, basestring):
            tag = tag.strip()
            if tag != "":
                tag, created = self.get_or_create(name=tag)
        elif isinstance(tag, self.model):
            pass
        else:
            raise ValueError("Cannot create tag %s" % tag)
        return tag

    def connect(self, tag, instance):
        tag = self.create_tag(tag)
        tag.connect(instance)

class TaggedItemManager(models.Manager):
    def filter_for_object(self, obj):
        query_set = self.filter_for_model(obj.__class__).filter(item_id=obj._get_pk_val())

        return query_set

    def filter_for_model(self, model, **kwargs):
        dscr = to_descriptor(model)
        table_name_quoted = quote_name(model._meta.db_table)

        query_set = self.filter(item_dscr=dscr)#\
            #.extra( select = { "%s_count" % model.__name__.lower(): "SELECT COUNT(*) FROM %(table)s WHERE %(table)s.id = item_id" % { "table" : table_name_quoted } } )

        if kwargs:
            query_set = self._extra(query_set, model, **kwargs)

        return query_set

    def _extra(self, query_set, model,**kwargs):
        table_name = model._meta.db_table
        table_name_quoted = quote_name(table_name)

        params = []
        for name, value in kwargs.iteritems():
            if isinstance(value, basestring):
                value = '"%s"' % value
            params.append((name, value))

        return query_set.extra(where=["%s.%s = %s" % (table_name_quoted, field, value) for field, value in params],
                                            tables=[table_name])

    def get_or_create_item(self, tag, instance):
        item, created = self.get_or_create(
                            tag=tag,
                            **self.get_item_connection(instance)
                        )
        return item, created

    def get_item_connection(self, instance):
        return {
            "item_id": instance._get_pk_val(),
            "item_dscr": to_descriptor(instance.__class__)
        }

class BaseTaggedModelManager(models.Manager):
    @property
    def descriptor(self):
        return to_descriptor(self.model)

    @property
    def table_name(self):
        return quote_name(self.model._meta.db_table)

    @property
    def taggeditems_table_name(self):
        from turbion.tags.models import TaggedItem

        return quote_name(TaggedItem._meta.db_table)

    def for_tag(sself, tag):
        return self.extra(
            where=[
                "%s.tag_id=%s" % (self.taggeditems_table_name, tag.id),
                "%s.item_dscr=%s" % (self.taggeditems_table_name, self.descriptor),
                "%s.item_id=%s.id" % (self.taggeditems_table_name, self.table_name)
            ],
            tables=[TaggedItem._meta.db_table]
        )
