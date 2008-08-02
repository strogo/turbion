# -*- coding: utf-8 -*-
from turbion.tags.models import Tag, TaggedItem
from django.contrib.contenttypes.models import ContentType

class ModelTagManager( object ):
    def __init__( self, instance ):
        self.instance = instance

    def all(self):
        return Tag.objects.filter_for_object( self.instance )

    def all_name( self ):
        return [ t.name for t in self.all() ]

    def _create_tag( self, tag ):
        if isinstance( tag, ( long, int) ):
            tag = Tag.objects.get( pk = tag)
        elif isinstance( tag, basestring ) and tag != "":
            tag, created = Tag.objects.get_or_create( name = tag.strip() )
        elif isinstance( tag, Tag ):
            pass
        else:
            raise ValueError
        return tag

    def _create_item( self ):
        return {
            "item_id" : self.instance._get_pk_val(),
            "item_ct" : ContentType.objects.get_for_model( self.instance.__class__ )
        }

    def add( self, *tags ):
        for tag in tags:
            tag = self._create_tag( tag )

            item = TaggedItem.objects.get_or_create( tag = tag,
                                                     **self._create_item() )

    def remove( self, *tags ):
        tags = map( self._create_tag, tags )

        item = TaggedItem.objects.filter( tag__in = tags,
                                          **self._create_item() )
        item.delete()

    def replace( self, *tags ):
        tags = map( self._create_tag, tags )

        my_tags = set( self.all() )

        for tag in tags:
            if tag in my_tags:
                my_tags.remove( tag )
            else:
                self.add( tag )

        if my_tags:
            self.remove( *list( my_tags ) )

class TagsField( object ):
    def __init__( self ):
        pass

    def __get__( self, instance, type = None ):
        return ModelTagManager( instance )

    def __set___( self, instance, value ):
        pass
