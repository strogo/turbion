# -*- coding: utf-8 -*-
from django.db import models, connection
from django.contrib.contenttypes.models import ContentType

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

class TaggedItemManager(models.Manager):
    def filter_for_object(self, obj):
        query_set = self.filter_for_model(obj.__class__).filter(item_id=obj._get_pk_val())

        return query_set

    def filter_for_model(self, model, **kwargs):
        ct = ContentType.objects.get_for_model(model)
        table_name_quoted = quote_name(model._meta.db_table)

        query_set = self.filter(item_ct=ct)#\
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
