# -*- coding: utf-8 -*-
from turbion.tags.models import Tag, TaggedItem
from django.contrib.contenttypes.models import ContentType

class ModelTagManager(object):
    def __init__(self, instance):
        self.instance = instance

    def all(self):
        return Tag.objects.filter_for_object(self.instance)

    def all_name(self):
        return [t.name for t in self.all()]

    def add(self, *tags):
        for tag in tags:
            Tag.objects.connect(tag, self.instance)

    def remove(self, *tags):
        tags = map(Tag.objects.create_tag, tags)

        item = TaggedItem.objects.filter(tag__in=tags,
                                         **TaggedItem.objects.get_item_connection(self.instance))
        item.delete()

    def replace( self, *tags ):
        tags = map(Tag.objects.create_tag, tags)

        my_tags = set(self.all())

        for tag in tags:
            if tag in my_tags:
                my_tags.remove(tag)
            else:
                self.add(tag)

        if my_tags:
            self.remove(*list(my_tags))

class TagsField(object):
    def __init__(self):
        pass

    def __get__(self, instance, type=None):
        return ModelTagManager(instance)

    def __set___(self, instance, value):
        ModelTagManager(instance).add(*value)
